import axios from "axios";

class ApiClient {
    constructor(baseURL) {
        this.client = axios.create({
            baseURL: baseURL,
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },

        })
        this.setCsrfToken()
    }

    async setCsrfToken() {
        try{
            const response = await this.client.get('/cars/get_csrf_token/')
            if(response.data.csrfToken){
                console.log("Csrf Token:", response.data.csrfToken)
                this.client.defaults.headers.common['X-CSRFToken'] = response.data.csrfToken
            }
        }
        catch(error){
            console.log('Fail get csrf',error)
        }

    }

    async get(url,config ={}) {
        return this.client.get(url,config)
    }

    async post(url,data = {}, config ={}) {
        if (!this.client.defaults.headers.common['X-CSRFToken']) {
            await this.setCsrfToken()
        }
        return this.client.post(url, data, config)
    }
}

const api = new ApiClient('http://127.0.0.1:8000/')

export default api