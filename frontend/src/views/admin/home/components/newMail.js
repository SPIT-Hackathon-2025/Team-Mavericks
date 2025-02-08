// Chakra imports
// Chakra imports
import {
    Flex,
    Stat,
    StatLabel,
    StatNumber,
    useColorModeValue,
    Text,
} from "@chakra-ui/react";
// Custom components
import Card from "components/card/Card.js";
// Custom icons
import React from "react";

export default function Default(props) {
    // const { from, subject, time, body}
    const textColor = useColorModeValue("secondaryGray.900", "white");
    const textColorSecondary = "secondaryGray.600";
    const subject ="We are thrilled to announce the International Summer Internship Program (ISIP) 2025, offering you an exceptional opportunity to gain global exposure and practical experience at prestigious universities. This year, we are excited to welcome two esteemed institutions to our program:"

    const body = "We are thrilled to announce the International Summer Internship Program (ISIP) 2025, offering you an exceptional opportunity to gain global exposure and practical experience at prestigious universities. This year, we are excited to welcome two esteemed institutions to our program:"

    return (
        <Card py='15px'>
            <Flex
                my='auto'
                h='100%'
                align={{ base: "center", xl: "start" }}
                justify={{ base: "center", xl: "center" }}>
                {/* start */}

                <Stat my='auto' ms={"18px"}>
                    <StatLabel
                        lineHeight='100%'
                        color={textColorSecondary}
                        fontSize={{
                            base: "sm",
                        }}>
                        tejashree.bhangale@gmail.com
                    </StatLabel>
                    <StatNumber
                        color={textColor}
                        fontSize={{
                            base: "xl",
                        }}>
                        {subject.length >30 ? `${subject.slice(0,50)}...`:subject }
                    </StatNumber>
                     {/* ( */}
                        <Flex align='center'>
                            <Text color='green.500' fontSize='xs' fontWeight='700' me='5px'>
                                12:30 pm
                            </Text>
                            <Text color='secondaryGray.600' fontSize='xs' fontWeight='400'>
                            {body.length > 200 ? `${body.slice(0, 200)}...` : subject}
                        </Text>
                        
                        </Flex>
                    {/* ) : null} */}
                </Stat>
                <Flex ms='auto' w='max-content'>
                    {/* {endContent} */}
                    {/* end */}
                </Flex>
            </Flex>
        </Card>
    );
}
