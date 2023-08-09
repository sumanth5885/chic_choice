function sendMessage() {
    var userInput = document.getElementById("user-input");
    var message = userInput.value;
    
    if (message.trim() !== "") {
      displayMessage("user", message);
      // Call a function to process user input and generate a response
      var response = getChatbotResponse(message);
      displayMessage("bot", response);
      userInput.value = "";
    }
  }
  
  function displayMessage(sender, message) {
    var chatDisplay = document.getElementById("chat-display");
    var messageElement = document.createElement("div");
    
    messageElement.classList.add(sender);
    messageElement.innerHTML = message;
    
    chatDisplay.appendChild(messageElement);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
  }
  
  function getChatbotResponse(message) {
    // Replace this with your own logic to generate chatbot responses based on user input
    if (message.includes("hello")) {
      return "Hello! How can I assist you today?";
    }
    
  else if(message.includes("founder")) {
      return "Koushik, Sumanth, Shubha";
  } 
  else if(message.includes("year")) {
    return "2023";
} 
  else if(message.includes("hi")) {
    return "Hello! ";
  }
  else if (message.includes("product")) {
      return "Sure! We have a wide range of products. How can I help you with a specific product?";
    } else {
      return "I'm sorry, I couldn't understand your request. Can you please rephrase it?";
    }
  }



  // function generateChatbotResponse(message) {
  //   var response;
  
  //   // Extracting product name from user input
  //   var productNamePattern = /(?:buy|purchase)\s+(.*)/i;
  //   var productNameMatch = message.match(productNamePattern);
  //   if (productNameMatch) {
  //     var productName = productNameMatch[1];
  //     // Process the extracted product name (e.g., check availability, add to cart, etc.)
  //     response = "You want to buy the product: " + productName;
  //     return response;
  //   }
  
  //   // Handling greetings
  //   var greetingsPattern = /hello|hi|hey/i;
  //   if (greetingsPattern.test(message)) {
  //     response = "Hello! How can I assist you today?";
  //     return response;
  //   }
  
  //   // Default response for unrecognized inputs
  //   response = "I'm sorry, I couldn't understand your request. Can you please rephrase it?";
  //   return response;
  // }
  
  