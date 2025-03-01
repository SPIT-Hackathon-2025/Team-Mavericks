import React from 'react';
import {
    Box,
    Button,
    Flex,
    Icon,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import Projects from './components/Projects';

const Today = () => {
    return (
        <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
            <Projects/>
        </Box>
    )
}

export default Today