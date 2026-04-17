import axios from "axios";
import {baseURL} from "./config.jsx";

class ApiClient {
    constructor(baseUrl) {
        this.client = axios.create({
            baseURL: baseUrl,
            withCredentials: true,
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        const token = localStorage.getItem("accessToken");
        if (token) {
            this.client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        }

        this.isRefreshing = false;
        this.failedRequests = [];

        this.client.interceptors.response.use(
            (response) => response,
            (error) => {
                const originalRequest = error.config;

                if (!error.response) {
                    return Promise.reject(error);
                }

                const isTokenError =
                    (error.response.status === 401 || error.response.status === 403) &&
                    error.response.data?.code === "token_not_valid";

                if (isTokenError && !originalRequest._retry) {
                    if (this.isRefreshing) {
                        return new Promise((resolve, reject) => {
                            this.failedRequests.push({
                                resolve,
                                reject,
                            });
                        })
                            .then((newAccessToken) => {
                                originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
                                return this.client(originalRequest);
                            })
                            .catch((err) => Promise.reject(err));
                    }

                    originalRequest._retry = true;
                    this.isRefreshing = true;

                    const refreshToken = localStorage.getItem("refreshToken");

                    if (!refreshToken) {
                        this.logout();
                        return Promise.reject(error);
                    }

                    return axios
                        .post(`${baseURL}cars/token/refresh/`, {
                            refresh: refreshToken,
                        })
                        .then((response) => {
                            const newAccessToken = response.data.access;

                            localStorage.setItem("accessToken", newAccessToken);
                            this.client.defaults.headers.common["Authorization"] = `Bearer ${newAccessToken}`;
                            originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

                            this.failedRequests.forEach((request) => {
                                request.resolve(newAccessToken);
                            });
                            this.failedRequests = [];

                            return this.client(originalRequest);
                        })
                        .catch((refreshError) => {
                            this.failedRequests.forEach((request) => {
                                request.reject(refreshError);
                            });
                            this.failedRequests = [];

                            this.logout();

                            return Promise.reject(refreshError);
                        })
                        .finally(() => {
                            this.isRefreshing = false;
                        });
                }

                return Promise.reject(error);
            }
        );

        this.setCsrfToken();
    }

    logout() {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        delete this.client.defaults.headers.common["Authorization"];
    }

    async setCsrfToken() {
        try {
            const response = await this.client.get("/cars/get_csrf_token/");
            if (response.data.csrfToken) {
                this.client.defaults.headers.common["X-CSRFToken"] = response.data.csrfToken;
            }
        } catch (error) {
            console.log("Failed on get csrf", error);
        }
    }

    async setTokenAuth() {
        try {
            const token = localStorage.getItem("accessToken");
            if (token) {
                this.client.defaults.headers.common["Authorization"] = `Bearer ${token}`;
            }
        } catch (error) {
            console.error("Error on auth set token", error);
        }
    }

    async get(url, config = {}) {
        return this.client.get(url, config);
    }

    async post(url, data = {}, config = {}) {
        if (!this.client.defaults.headers.common["X-CSRFToken"]) {
            await this.setCsrfToken();
        }
        return this.client.post(url, data, config);
    }

    async patch(url, data = {}, config = {}) {
        if (!this.client.defaults.headers.common["X-CSRFToken"]) {
            await this.setCsrfToken();
        }
        return this.client.patch(url, data, config);
    }

    async put(url, data = {}, config = {}) {
        if (!this.client.defaults.headers.common["X-CSRFToken"]) {
            await this.setCsrfToken();
        }
        return this.client.put(url, data, config);
    }

    async delete(url, config = {}) {
        if (!this.client.defaults.headers.common["X-CSRFToken"]) {
            await this.setCsrfToken();
        }
        return this.client.delete(url, config);
    }
}

const api = new ApiClient(baseURL);

export default api;