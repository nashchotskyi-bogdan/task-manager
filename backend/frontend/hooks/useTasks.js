let tasks = [];
async function loadTasks() {
    tasks = await TasksAPI.getAll();
    return tasks;
}
function getTasks() {
    return tasks;
}