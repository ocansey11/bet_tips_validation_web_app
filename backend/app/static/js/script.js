// Add an event listener to execute code when the DOM content has fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Get the search input element by its ID
    const searchInput = document.getElementById('search-input');
    // Get the table element by its ID
    const dataTable = document.getElementById('data-table');
    // Select all table rows within the tbody of the table
    const tableRows = dataTable.querySelectorAll('tbody tr');

    // Add an event listener to the search input that triggers on every input change
    searchInput.addEventListener('input', () => {
        // Retrieve and convert the search input value to lowercase for case-insensitive comparison
        const searchTerm = searchInput.value.toLowerCase();

        // Iterate over each table row
        tableRows.forEach(row => {
            // Select all cells within the current row
            const cells = row.querySelectorAll('td');
            // Extract and concatenate text content from all cells in the row, converted to lowercase
            const rowText = Array.from(cells).map(cell => cell.textContent.toLowerCase()).join(' ');

            // Check if the row's text content includes the search term
            if (rowText.includes(searchTerm)) {
                // Display the row if the search term is found
                row.style.display = '';
            } else {
                // Hide the row if the search term is not found
                row.style.display = 'none';
            }
        });
    });
});
