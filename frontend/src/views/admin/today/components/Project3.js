import {
    Box,
    Flex,
    Icon,
    Link,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
import Card from "components/card/Card.js";
import React, { useState } from "react";
import { MdExpand } from "react-icons/md";

export default function Project(props) {
    const { event, ...rest } = props;
    const [showBody, setShowBody] = useState(false);

    // Chakra Color Mode
    const textColorPrimary = useColorModeValue("secondaryGray.900", "white");
    const textColorSecondary = "gray.400";
    const brandColor = useColorModeValue("brand.500", "white");
    const bg = useColorModeValue("white", "navy.700");

    const handleSeeDetails = () => {
        setShowBody(!showBody);
    };

    return (
        <Card bg={bg} {...rest} p="14px">
            <Flex align="center" direction={{ base: "column", md: "row" }}>
                <Box mt={{ base: "10px", md: "0" }}>
                    <Text color={textColorPrimary} fontWeight="500" fontSize="md" mb="4px">
                        {event.summary || "No Title"}
                    </Text>
                    <Text fontWeight="500" color={textColorSecondary} fontSize="sm" me="4px">
                        {event.start.dateTime|| "No Due Date"}{" "}
                        <Link fontWeight="500" color={brandColor} href={`mailto:${event.creator.email}`} fontSize="sm">
                            {event.creator.email || "No Assignee"}
                        </Link>
                    </Text>
                </Box>
                <Link href="#" variant="no-hover" me="16px" ms="auto" p="0px !important" onClick={handleSeeDetails}>
                    <Icon as={MdExpand} color="secondaryGray.500" h="18px" w="18px" />
                </Link>
            </Flex>
            {showBody && (
                <Text>
                    {event.description || "No Description"}
                </Text>
            )}
        </Card>
    );
}
