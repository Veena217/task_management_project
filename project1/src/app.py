from flask import Flask, request, jsonify
from storageutils import MySQLManager  # Import your custom MySQLManager for query execution
from variables import CONFIG  # Import your DB config
import mysql.connector

app = Flask(__name__)

# Function to insert a task into the database
def create_task(title, description, status):
    query = "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s);"
    values = (title, description, status)
    try:
        MySQLManager.execute_query(query, values, **CONFIG['database']['vjit'])
        return {"message": "Task Created"}, 201
    except mysql.connector.Error as error:
        print(f"Database Error: {error}")
        return {"message": "Database Error"}, 500

# Function to fetch all tasks from the database
def fetch_all_tasks():
    query = "SELECT * FROM tasks;"
    tasks = []
    try:
        connection = MySQLManager.get_connection(**CONFIG['database']['vjit'])
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            
            for task in result:
                tasks.append({
                    "id": task[0],
                    "title": task[1],
                    "description": task[2],
                    "status": task[3],
                    "created_at": task[4]
                })
            cursor.close()
            connection.close()
        else:
            print("Database connection failed")
            return {"message": "Database connection error"}, 500
    except Exception as error:
        print(f"Error fetching tasks: {error}")  # Print the full error message
        return {"message": f"Database Error: {error}"}, 500  # Return the detailed error for debugging
    
    return tasks


# Function to update a task in the database
def update_task(task_id, title, description, status):
    query = "UPDATE tasks SET title = %s, description = %s, status = %s WHERE id = %s;"
    values = (title, description, status, task_id)
    try:
        connection = MySQLManager.get_connection(**CONFIG['database']['vjit'])
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()  # Commit the transaction
        cursor.close()
        connection.close()
        return {"message": "Task Updated"}, 200
    except mysql.connector.Error as error:
        print(f"Error updating task: {error}")
        return {"message": "Database Error"}, 500

# Function to delete a task from the database
def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = %s;"
    try:
        connection = MySQLManager.get_connection(**CONFIG['database']['vjit'])
        cursor = connection.cursor()
        cursor.execute(query, (task_id,))
        connection.commit()  # Commit the transaction
        cursor.close()
        connection.close()
        return {"message": "Task Deleted"}, 204
    except mysql.connector.Error as error:
        print(f"Error deleting task: {error}")
        return {"message": "Database Error"}, 500

# Route for creating a new task
@app.route('/tasks', methods=['POST'])
def create_task_route():
    _input = request.json
    title = _input.get("title", "")
    description = _input.get("description", "")
    status = _input.get("status", "pending")
    
    if not title or not description:  # Basic validation
        return jsonify({"message": "Title and Description are required"}), 400
    
    response, status_code = create_task(title, description, status)
    return jsonify(response), status_code

# Route for fetching all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks_route():
    tasks = fetch_all_tasks()
    if isinstance(tasks, dict):  # Check for error message
        return jsonify(tasks), 500
    return jsonify(tasks), 200

# Route for updating a task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    _input = request.json
    title = _input.get("title", "")
    description = _input.get("description", "")
    status = _input.get("status", "pending")

    if not title or not description:  # Basic validation
        return jsonify({"message": "Title and Description are required"}), 400

    response, status_code = update_task(task_id, title, description, status)
    return jsonify(response), status_code

# Route for deleting a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    response, status_code = delete_task(task_id)
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)  # Set debug=True for detailed error messages
