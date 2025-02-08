import React,{useState} from 'react';
// Chakra imports
import {
  Box,
  Button,
  Flex,
  Icon,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import NewMail from './components/newMail';
import Step from "./components/Step1";


const Index = () => {
  const [processing, setProcessing] = useState(true);

  return (
    <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
      

      <div>
        <NewMail />
        <Step processing={processing} />
        
      <Button
        me='100%'
        mb='50px'
        w='140px'
        minW='140px'
        mt={{ base: "20px", "2xl": "auto" }}
        variant='brand'
          fontWeight='500'
          onClick={()=>{setProcessing(false)}}
        >
        Publish now
      </Button>
      </div>
      </Box>
  )
}

export default Index