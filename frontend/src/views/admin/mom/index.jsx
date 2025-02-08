import React from 'react';
import {
    Box,
    Button,
    Flex,
    Icon,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import MeetCard from './components/meetingCard'


const Mom = () => {
    return (
        <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>

            <MeetCard />
        </Box>

    )
}

export default Mom