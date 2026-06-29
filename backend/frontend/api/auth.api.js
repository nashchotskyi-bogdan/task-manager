const BASE = CONFIG.API_BASE;
window.AuthAPI = {
    login: (data) =>
        request(BASE + "/token/", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    register: (data) =>
        request(BASE + "/register/", {
            method: "POST",
            body: JSON.stringify(data)
        })
};