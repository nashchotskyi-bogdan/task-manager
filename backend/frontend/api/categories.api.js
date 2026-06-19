const BASE = CONFIG.API_BASE;
export const CategoriesAPI = {
    getAll: () =>
        request(BASE + "/categories/"),
    create: (data) =>
        request(BASE + "/categories/", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    update: (id, data) =>
        request(BASE + "/categories/" + id + "/", {
            method: "PATCH",
            body: JSON.stringify(data)
        }),
    delete: (id) =>
        request(BASE + "/categories/" + id + "/", {
            method: "DELETE"
        })
};