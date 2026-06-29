function getToken() {
    return localStorage.getItem("access");
}
function headers() {
    return {
        "Content-Type": "application/json",
        ...(getToken() && {
            "Authorization": "Bearer " + getToken()
        })
    };
}
async function request(url, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {
            ...headers(),
            ...(options.headers || {})
        }
    });
    if (!res.ok) {
        const error = await res.text();
        throw new Error(error);
    }
    return res.json();
}
window.request = request;