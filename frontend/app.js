// CONCEPT: This endpoint represents your API Gateway entry point.
// You must replace this placeholder string with your real Invoke URL in Phase 5!
const API_URL = "https://cil6wpo2jk.execute-api.us-east-1.amazonaws.com/orders";

async function submitOrder() {
    // 1. Fetch values from the HTML input fields
    const itemName = document.getElementById('itemName').value;
    
    // 2. Note: Generate a unique ID on the client side 
    // to use as our DynamoDB Partition Key (Primary Key).
    const orderId= "ORD-" + Math.floor(Math.random() * 10000);
    const msgField = document.getElementById('msg');

    // Inform user the data is traveling to the cloud
    msgField.innerText = "Sending payload to AWS...";

    try {
        // 3. Perform an asynchronous HTTP POST request to API Gateway
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 
                // Tells API Gateway and Lambda that we are sending JSON data
                'Content-Type': 'application/json' 
            },
            // Convert JavaScript object into a text string for transit
            body: JSON.stringify({ orderId: orderId, itemName: itemName })
        });
        
        // 4. Parse the JSON confirmation response returned from AWS Lambda
        const data = await response.json();
        
        // Update screen with success message from backend
        msgField.innerText = data.message || "Order processed successfully!";
        
    } catch (err) {
        // Triggers if API Gateway is down, CORS is broken, or the URL is wrong
        msgField.innerText = "API Error. Check browser console logs or CORS settings.";
        console.error("Network Error Details:", err);
    }
}

