function requireAuth() {
    const token = localStorage.getItem("access");
    if (!token) {
        window.location.href = "/";
    }
}
window.requireAuth = requireAuth;