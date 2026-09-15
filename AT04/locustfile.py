from locust import HttpUser, between, constant, task


class LoadTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_endpoint(self):
        self.client.get("/api/test")


class StressTestUser(HttpUser):
    wait_time = constant(0.1)

    @task
    def test_endpoint(self):
        self.client.get("/api/test")
