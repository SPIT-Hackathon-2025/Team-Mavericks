import React, { useState, useEffect } from "react";
// Chakra imports
import { Box, Button } from "@chakra-ui/react";
import NewMail from "./components/newMail";
import Step from "./components/Step1";

const Index = () => {
  const [processing, setProcessing] = useState(true);
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]); // Store WebSocket messages

  useEffect(() => {
    // Connect to WebSocket server
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connected!");
      ws.send("Client!"); // Send a message to the server
    };

    ws.onmessage = (event) => {
      console.log("Received:", event.data);
      setMessages((prev) => [...prev, event.data]); // Store received messages
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected!");
    };

    setSocket(ws);

    return () => {
      ws.close(); // Clean up WebSocket connection on component unmount
    };
  }, []);

  const handlePublish = () => {
    setProcessing(false);
    if (socket) {
      socket.send("Start email processing!"); // Send a message to the WebSocket server
    }
  };

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <div>
        <NewMail />
        <Step processing={processing} />

        <Button
          me="100%"
          mb="50px"
          w="140px"
          minW="140px"
          mt={{ base: "20px", "2xl": "auto" }}
          variant="brand"
          fontWeight="500"
          onClick={handlePublish}
        >
          Publish now
        </Button>

        {/* Display WebSocket Messages */}
        <Box mt="20px" p="10px" border="1px solid gray">
          <strong>WebSocket Messages:</strong>
          {messages.map((msg, index) => (
            <p key={index}>{msg}</p>
          ))}
        </Box>
      </div>
    </Box>
  );
};

export default Index;
