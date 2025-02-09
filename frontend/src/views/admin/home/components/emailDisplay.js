// EmailDisplay.js
import React from 'react';
import { Box, Text, VStack, Divider, Badge } from '@chakra-ui/react';

const EmailDisplay = ({ emails }) => {
  return (
    <VStack spacing={4} align="stretch">
      {emails.map((email, index) => (
        <Box key={index} p={4} borderWidth={1} borderRadius="md" boxShadow="md">
          <Text fontWeight="bold">{email.subject}</Text>
          <Text color="gray.500">{`From: ${email.from}`}</Text>
          <Text color="gray.500">{`To: ${email.to}`}</Text>
          <Text color="gray.500">{`Date: ${new Date(email.date).toLocaleString()}`}</Text>
          <Divider my={2} />
          <Text>{email.body || "No message body."}</Text>
          {email.attachments.length > 0 && (
            <Text color="blue.500">{`Attachments: ${email.attachments.join(', ')}`}</Text>
          )}
          <Badge colorScheme={email.categorized === 'Task Assignment' ? 'green' : 'blue'}>
            {email.categorized}
          </Badge>
        </Box>
      ))}
    </VStack>
  );
};

export default EmailDisplay;