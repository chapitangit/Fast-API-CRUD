

$(document).ready(function() {
    $('#btn_save_employee').on('click', function(event) {
        event.preventDefault();

        // Gather form data
        const employeeData = {
            employee_id: $('#employee_id').val(),
            employee_name: $('#employee_name').val(),
            division: $('#division').val(),
            position: $('#position').val(),
            status: $('#is_active').val() === 'true'
        };

        // GraphQL mutation
        const query = `
        mutation {
            insertEmployee(employeeDetails: {
                employeeId: "${employeeData.employee_id}",
                employeeName: "${employeeData.employee_name}",
                division: "${employeeData.division}",
                position: "${employeeData.position}",
                status: ${employeeData.status}
            })
        }`;

        // AJAX request
        $.ajax({
            url: '/graphql',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: query }),
            success: function(response) {
                if (response.data && response.data.insertEmployee) {
                    if (typeof response.data.insertEmployee === 'string') {
                        window.alert(response.data.insertEmployee);
                        window.location.assign("/employee-list/");
                    } else {
                        window.alert("Employee inserted successfully!");
                        window.location.assign("/employee-list/");
                    }
                } else if (response.errors) {
                    const errorMessage = response.errors[0].message;
                    if (errorMessage.includes("already exists")) {
                        window.alert("Employee with this ID or name already exists");
                    } else {
                        window.alert(`Error: ${errorMessage}`);
                    }
                }
            },
            error: function(xhr, status, error) {
                window.alert("Error: " + error);
            }
        });
    });
});


// this function is to display data into the table

$(document).ready(function() {
    // Function to fetch and display employee data
    function displayEmployeeData() {
        // GraphQL query to fetch all employees
        const query = `
        query {
            getAllEmployees {
                employeeId
                employeeName
                division
                position
                status
            }
        }`;

        // AJAX request
        $.ajax({
            url: '/graphql',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: query }),
            success: function(response) {
                if (response.data && response.data.getAllEmployees) {
                    const employees = response.data.getAllEmployees;

                    // Clear existing table rows
                    $('#table_employee_list tbody').empty();

                    // Populate table with employee data
                    employees.forEach(function(employee) {
                        const row = `
                        <tr>
                            <td>${employee.employeeId}</td>
                            <td>${employee.employeeName}</td>
                            <td>${employee.division}</td>
                            <td>${employee.position}</td>
                            <td>${employee.status ? 'Active' : 'Inactive'}</td>
                            <td>
                                <!-- Add action buttons if needed -->
                            </td>
                        </tr>`;
                        $('#table_employee_list tbody').append(row);
                    });
                } else if (response.errors) {
                    const errorMessage = response.errors[0].message;
                    window.alert(`Error: ${errorMessage}`);
                }
            },
            error: function(xhr, status, error) {
                window.alert("Error: " + error);
            }
        });
    }

    // Call the function to initially display employee data
    displayEmployeeData();
});


