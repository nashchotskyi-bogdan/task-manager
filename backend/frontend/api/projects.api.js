const BASE = CONFIG.API_BASE;
export const ProjectsAPI = {
    getAll: () =>
        request(BASE + "/projects/"),
    create: (data) =>
        request(BASE + "/projects/", {
            method: "POST",
            body: JSON.stringify(data)
        }),
    update: (id, data) =>
        request(BASE + "/projects/" + id + "/", {
            method: "PATCH",
            body: JSON.stringify(data)
        }),
    delete: (id) =>
        request(BASE + "/projects/" + id + "/", {
            method: "DELETE"
        })
};