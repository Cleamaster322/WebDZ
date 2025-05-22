import axios from 'axios'
import { baseURL} from "./config.jsx";


class ApiClient {
  constructor(baseUrl) {
    this.client = axios.create({
      baseURL: baseUrl,
      withCredentials: true,
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    })

    const token = localStorage.getItem('accessToken')
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    this.isRefreshint = false
    this.failedRequests = []

    this.client.interceptors.response.use(
        (response) => response,
        async (error) => {
          const originalRequest = error.config

          console.log(error.response,12321312)

          if (
            (error.response?.status === 401 || error.response?.status === 403) &&
            error.response.data?.code === 'token_not_valid' &&
            !originalRequest._retry
          ) {
            if (this.isRefreshint) {
              return new Promise((resolve, reject) => {
                this.failedRequests.push((token) => {
                  originalRequest.headers['Authorization'] = `Bearer ${token}`
                  resolve(this.client(originalRequest))
                })
              })
            }

            this.isRefreshint = true
            originalRequest._retry = true

            try{
              const refreshToken = localStorage.getItem('refreshToken')
              const response = await axios.post(`${baseURL}cars/token/refresh/`, {"refresh":refreshToken})

              const newAccessToken = response.data.access
              localStorage.setItem('accessToken', newAccessToken)
              console.log(3213213123123)
              this.client.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`
              originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`

              const retryResponse = await this.client(originalRequest)

              this.failedRequests.forEach((callback) => callback())
              this.failedRequests = []

              return retryResponse

            }catch(refreshError){
              console.error(refreshError)
              localStorage.removeItem('accessToken')
              localStorage.removeItem('refreshToken')
              return Promise.reject(refreshError)
            }
            finally {
              this.isRefreshint = false
            }
          }
        }
    )

    this.setCsrfToken()

  }

  async setCsrfToken() {
    try {
      const response = await this.client.get('/cars/get_csrf_token/')
      if (response.data.csrfToken) {
        this.client.defaults.headers.common['X-CSRFToken'] = response.data.csrfToken
      }
    } catch (error) {
      console.log('Failed on get csrf', error)
    }
  }

  async setTokenAuth() {
    try {
      const token = localStorage.getItem('accessToken')
      if (token) {
        this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    } catch (error) {
      console.error('Error on auth set token', error)
    }
  }

  async get(url, config = {}) {
    return this.client.get(url, config)
  }

  async post(url, data = {}, config = {}) {
    if (!this.client.defaults.headers.common['X-CSRFToken']) {
      await this.setCsrfToken()
    }
    return this.client.post(url, data, config)
  }
}

const api = new ApiClient(baseURL)

export default api