import { TasksAPI } from "../api/tasks.api.js";
let tasks = [];
export async function loadTasks() {
    tasks = await TasksAPI.getAll();
    return tasks;
}
export function getTasks() {
    return tasks;
}