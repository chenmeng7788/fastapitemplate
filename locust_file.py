import os
import random
import string
import uuid
from locust import HttpUser, task, between, TaskSet, tag
from locust.exception import StopUser
from locust.contrib.fasthttp import FastHttpUser


# 工具函数：生成随机测试数据
def generate_random_name():
    """生成随机姓名（拼接UUID后缀，避免重复）"""
    first_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace"]
    last_names = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller"]
    unique_suffix = uuid.uuid4().hex[:8]  # 增加UUID后缀，彻底避免重复
    return f"{random.choice(first_names)}_{random.choice(last_names)}_{unique_suffix}"


def generate_random_email():
    """生成随机邮箱（UUID前缀，确保唯一）"""
    username = uuid.uuid4().hex
    domains = ["example.com", "test.com", "demo.org"]
    return f"{username}@{random.choice(domains)}"


def generate_random_password():
    """生成随机密码"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# 定义任务集（存储user_id）
class HelloWorld(TaskSet):
    user_id = None  # 记录当前任务集创建的用户ID

    @tag("create_user")
    @task(2)
    def create_user(self):
        if self.user_id:
            return  # 已创建用户，跳过

        user_data = {
            "full_name": generate_random_name(),
            "email": generate_random_email(),
            "hashed_password": generate_random_password()
        }

        response = self.client.post(
            "/api/v1/users",
            json=user_data,
            name="/api/users"
        )

        try:
            assert response.status_code == 200, f"创建用户失败，状态码：{response.status_code}"
            self.user_id = response.json().get("id")
            assert self.user_id, "响应中未返回用户ID"
        except AssertionError as e:
            self.user.environment.events.request.fire(
                request_type="POST",
                name="/api/users",
                response_time=response.elapsed.total_seconds() * 1000,
                exception=e,
                success=False
            )

    @tag("get_user")
    @task(3)
    def get_user(self):
        if not self.user_id:
            return

        response = self.client.get(
            f"/api/v1/users/{self.user_id}",
            name="/api/users/[id]"
        )

        try:
            assert response.status_code == 200, f"查询用户失败，状态码：{response.status_code}"
            assert response.json().get("id") == self.user_id, "用户ID不匹配"
        except AssertionError as e:
            self.user.environment.events.request.fire(
                request_type="GET",
                name="/api/users/[id]",
                response_time=response.elapsed.total_seconds() * 1000,
                exception=e,
                success=False
            )

    @tag("update_user")
    @task(2)
    def update_user(self):
        if not self.user_id:
            return

        update_data = {"email": generate_random_email(), "ful_name": generate_random_name() }
        response = self.client.put(
            f"/api/v1/users/{self.user_id}",
            json=update_data,
            name="/api/users/[id]"
        )

        try:
            assert response.status_code == 200, f"更新用户失败，状态码：{response.status_code}"
            # 注意：若接口返回的密码是加密后的，需调整断言逻辑（避免直接对比明文）
            # assert updated_user.get("hashed_password") == update_data["hashed_password"]
        except AssertionError as e:
            self.user.environment.events.request.fire(
                request_type="PUT",
                name="/api/users/[id]",
                response_time=response.elapsed.total_seconds() * 1000,
                exception=e,
                success=False
            )

    @tag("get_all_users")
    @task(4)
    def get_all_users(self):
        skip = random.randint(1, 5)
        limit = random.choice([10, 20, 50])

        response = self.client.get(
            f"/api/v1/users?page={skip}&per_page={limit}",
            name="/api/users?page&per_page"
        )

        try:
            assert response.status_code == 200, f"查询所有用户失败，状态码：{response.status_code}"
        except AssertionError as e:
            self.user.environment.events.request.fire(
                request_type="GET",
                name="/api/users?page&per_page",
                response_time=response.elapsed.total_seconds() * 1000,
                exception=e,
                success=False
            )

    @tag("delete_user")
    @task(1)
    def delete_user(self):
        if not self.user_id:
            return

        response = self.client.delete(
            f"/api/v1/users/{self.user_id}",
            name="/api/users/[id]"
        )

        try:
            assert response.status_code == 200, f"删除用户失败，状态码：{response.status_code}"
            self.user_id = None  # 重置ID
        except AssertionError as e:
            self.user.environment.events.request.fire(
                request_type="DELETE",
                name="/api/users/[id]",
                response_time=response.elapsed.total_seconds() * 1000,
                exception=e,
                success=False
            )


# 主用户类
class UserManagementUser(FastHttpUser):
    wait_time = between(2, 4)
    tasks = [HelloWorld]  # 关联任务集
    auth_token = None

    def on_start(self):
        """用户启动时设置请求头（无需登录）"""
        self.client.headers = {"X-Token": "coneofsilence"}

    def on_stop(self):
        """用户结束时：删除当前用户创建的测试数据"""
        # 关键：通过任务集实例获取user_id（tasks[0]即HelloWorld实例）
        task_set = self.tasks[0]  # 获取当前用户的任务集实例
        if hasattr(task_set, "user_id") and task_set.user_id:
            # 调用删除接口清理测试用户
            response = self.client.delete(
                f"/api/v1/users/{task_set.user_id}",
                name="/api/users/[id] (cleanup)"  # 单独命名，便于统计清理结果
            )
            # 记录清理结果（成功/失败）
            if response.status_code == 200:
                self.environment.events.request.fire(
                    request_type="DELETE",
                    name="/api/users/[id] (cleanup)",
                    response_time=response.elapsed.total_seconds() * 1000,
                    response_length=len(response.content),
                    success=True
                )
                print(f"清理测试用户成功，ID：{task_set.user_id}")
            else:
                self.environment.events.request.fire(
                    request_type="DELETE",
                    name="/api/users/[id] (cleanup)",
                    response_time=response.elapsed.total_seconds() * 1000,
                    exception=Exception(f"清理失败，状态码：{response.status_code}"),
                    success=False
                )
                print(f"清理测试用户失败，ID：{task_set.user_id}，状态码：{response.status_code}")
        else:
            print("无需要清理的测试用户（未创建或已删除）")

        # 关闭请求会话（可选，Locust会自动处理）
        self.client.close()


if __name__ == '__main__':
    # 运行Locust（仅测试create_user标签，可根据需要修改）
    os.system("locust -f locust_file.py -H http://localhost:8000")