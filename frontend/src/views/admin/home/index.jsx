import React, { useState, useEffect } from "react";
import { Box, Button } from "@chakra-ui/react";
import NewMail from "./components/newMail";
import Step from "./components/Step1";
import EmailDisplay from "./components/emailDisplay"; // Import the new component

const Index = () => {
  const [processing, setProcessing] = useState(true);
  const [socket, setSocket] = useState(null);
  const [messages, setMessages] = useState([]);
  const [emails, setEmails] = useState([]); // State to hold email data
  const [mailDetails, setMailDetails] = useState({});
  const [newMails, setNewMails] = useState({});


  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws");

    ws.onopen = () => {
      console.log("WebSocket connected!");
      ws.send("Client!");
    };

    ws.onmessage = (event) => {
      console.log("Received:", event.data);
      if(event.data.startsWith("new_email ")) {
        event = event.data.replace("new_email ", "");
        setNewMails(JSON.parse(event));
      }
      
      // const emailData = JSON.parse(event.data)\\; // Assuming the server sends JSON
      // setEmails((prev) => [...prev, ...emailData]); // Update emails state
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected!");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  const handlePublish = () => {
    setProcessing(false);
    if (socket) {
      socket.send("Start email processing!");
    }
  };

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      <div>
        {/* <NewMail newMails={newMails} /> */}
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

        {/* Display Emails */}
        {/* <EmailDisplay emails={emails} /> */}

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