export function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
export function isStrongPassword(password) {
    return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(password);
}
export function validateLogin({ username, password }) {
    const errors = {};
    if (!username || username.trim().length < 3) {
        errors.username = "Username must be at least 3 characters";
    }
    if (!password || password.length < 6) {
        errors.password = "Password is too short";
    }
    return {
        valid: Object.keys(errors).length === 0,
        errors
    };
}
export function validateRegister({ username, email, password }) {
    const errors = {};
    if (!username || username.trim().length < 3) {
        errors.username = "Username must be at least 3 characters";
    }
    if (!isValidEmail(email)) {
        errors.email = "Invalid email format";
    }
    if (!isStrongPassword(password)) {
        errors.password =
            "Password must contain uppercase, lowercase, number and special character";
    }
    return {
        valid: Object.keys(errors).length === 0,
        errors
    };
}