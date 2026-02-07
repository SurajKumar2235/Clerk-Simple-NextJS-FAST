// frontend/utils/apiTester.ts

type TestResult = {
    endpoint: string;
    status: number;
    success: boolean;
    data: any;
    duration: number;
};

export class ApiTester {
    private baseUrl: string;
    private getToken: () => Promise<string | null>;

    constructor(baseUrl: string, getToken: () => Promise<string | null>) {
        this.baseUrl = baseUrl.replace(/\/$/, "");
        this.getToken = getToken;
    }

    private async log(message: string, data?: any) {
        console.log(`[API TEST] ${message}`, data || "");
    }

    async testEndpoint(
        method: "GET" | "POST" | "PUT" | "DELETE",
        endpoint: string,
        payload?: any,
        expectedStatus: number = 200
    ): Promise<TestResult> {
        const url = `${this.baseUrl}/${endpoint.replace(/^\//, "")}`;
        this.log(`Testing ${method} ${url}`);

        const token = await this.getToken();
        if (!token) {
            this.log("❌ No Auth Token Available");
            return { endpoint, status: 0, success: false, data: "No Token", duration: 0 };
        }

        const startTime = performance.now();
        try {
            const res = await fetch(url, {
                method,
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: payload ? JSON.stringify(payload) : undefined
            });

            const duration = performance.now() - startTime;
            const data = await res.json();

            this.log(`Status: ${res.status} (${duration.toFixed(2)}ms)`);

            if (res.status === expectedStatus) {
                this.log("✅ PASSED");
            } else {
                this.log(`❌ FAILED. Expected ${expectedStatus}, got ${res.status}`, data);
            }

            return {
                endpoint,
                status: res.status,
                success: res.status === expectedStatus,
                data,
                duration
            };

        } catch (error) {
            const duration = performance.now() - startTime;
            this.log(`❌ EXCEPTION:`, error);
            return {
                endpoint,
                status: 0,
                success: false,
                data: error,
                duration
            };
        }
    }
}
