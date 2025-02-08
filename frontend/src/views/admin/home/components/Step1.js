// Chakra imports
import {
    Box,
    Flex,
    Icon,
    Progress,
    Text,
    useColorModeValue,
    Spinner,
} from "@chakra-ui/react";
// Custom components
import Card from "components/card/Card.js";
import IconBox from "components/icons/IconBox";
import Menu from "components/menu/MainMenu";
import React from "react";
// Assets
import { MdOutlineDoneOutline } from "react-icons/md";

export default function Banner(props) {
    const { used, total, processing } = props;
    // Chakra Color Mode
    const textColorPrimary = useColorModeValue("secondaryGray.900", "white");
    const brandColor = useColorModeValue("brand.500", "white");
    const textColorSecondary = "gray.400";
    const box = useColorModeValue("secondaryGray.300", "whiteAlpha.100");

    return (
        <Card mb={{ base: "0px", lg: "20px" }} w="200px"  align='center' m={"5"}>
            <Flex w='100%'>
                <Menu ms='auto' />
            </Flex>
            <IconBox
                mx='auto'
                h='100px'
                w='100px'
                icon={
                    processing ? (
                        <Spinner color={brandColor} h='46px' w='46px' />
                    ) : (
                            <Icon as={MdOutlineDoneOutline} color={brandColor} h='46px' w='46px' />
                    )
                }
                bg={box}
            />
            <Text color={textColorPrimary} fontWeight='bold' fontSize='2xl' mt='10px'>
                {processing ? "Processing" : "Completed"}
            </Text>
            <Text
                color={textColorSecondary}
                fontSize='md'
                maxW={{ base: "20%", xl: "80%", "3xl": "60%" }}
                mx='auto'>
                {processing ? "Processing your incoming mail, just a moment..." : "Your mail has been processed successfully!"}
            </Text>
        </Card>
    );
}
