import axios from "axios"

const HOST = 'https://chinhhoangcong17.pythonanywhere.com'

export const endpoints = {
    'activities': '/activities/',
    'trainingPoints' : '/trainingPoints/' 
}

export const authApi = () => {
    return axios.create({
        baseURL: HOST,
        headers: {
            'Authorization': `Bearer ...`
        }
    })
}

export default axios.create({
    baseURL: HOST
})