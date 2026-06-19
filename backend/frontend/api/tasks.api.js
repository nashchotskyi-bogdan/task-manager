const BASE = CONFIG.API_BASE;
export const TasksAPI = {
    getAll: () => request(BASE + "/tasks/"),
    create: (data) =>
        request(BASE + "/tasks/", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    update: (id, data) =>
        request(BASE + "/tasks/" + id + "/", {
            method: "PATCH",
            body: JSON.stringify(data)
        }),
    delete: (id) =>
        request(BASE + "/tasks/" + id + "/", {
            method: "DELETE"
        })
};