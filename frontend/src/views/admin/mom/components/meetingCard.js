import {
    Button,
    Card,
    CardHeader,
    CardBody,
    CardFooter,
    Heading,
    Text,
    Avatar,
    Stack,
    Flex,
    Icon,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalFooter,
    useDisclosure
} from "@chakra-ui/react";
import { MdAccessTime, MdLocationOn } from "react-icons/md";
import { useColorModeValue } from "@chakra-ui/react";

const Demo = () => {
    const { isOpen, onOpen, onClose } = useDisclosure(); // Modal control
    const textColorPrimary = useColorModeValue("secondaryGray.900", "white");


    return (
        <>
            {/* Meeting Card */}
            <Card width="350px" boxShadow="lg" borderRadius="lg" p={4}>
                {/* Header with Avatar & Title */}
                <CardHeader>
                    <Stack direction="row" align="center" spacing={3}>
                        <Avatar name="Nue Camp" src="https://picsum.photos/200/300" size="md" />
                        <Text
                            color={textColorPrimary}
                            fontWeight='bold'
                            fontSize='2xl'
                            mt='10px'
                            mb='4px'>
                            Project syhc meeting
                        </Text>
                    </Stack>
                </CardHeader>

                {/* Meeting Details */}
                <CardBody>
                    <Stack spacing={3}>
                        <Flex align="center" gap={2}>
                            <Icon as={MdAccessTime} color="blue.500" />
                            <Text fontSize="sm" color={textColorPrimary}
                            >10:30 AM - 11:30 AM, July 25, 2025</Text>
                        </Flex>

                        <Flex align="center" gap={2}>
                            <Icon as={MdLocationOn} color="red.500" />
                            <Text fontSize="sm" color={textColorPrimary}
                            >Google Meet</Text>
                        </Flex>

                        <Text fontSize="sm" color={textColorPrimary}
                        >
                            Discussion on project updates, blockers, and next steps.
                        </Text>
                    </Stack>
                </CardBody>

                {/* Footer with Action Buttons */}
                <CardFooter display="flex" justifyContent="flex-end">
                    <Button variant="outline" colorScheme="blue" onClick={onOpen}>View</Button>
                </CardFooter>
            </Card>

            {/* Minutes of the Meeting Modal */}
            <Modal isOpen={isOpen} onClose={onClose} size="md">
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Minutes of Meeting</ModalHeader>
                    <ModalBody>
                        <Stack spacing={3}>
                            <Text><b>Agenda:</b> Discuss project updates and blockers.</Text>
                            <Text><b>Key Points:</b></Text>
                            <Text>- Progress update from each team member.</Text>
                            <Text>- Challenges faced and potential solutions.</Text>
                            <Text>- Next steps and action items.</Text>
                            <Text>- Follow-up meeting scheduled for August 1, 2025.</Text>
                        </Stack>
                    </ModalBody>
                    <ModalFooter>
                        <Button colorScheme="blue" mr={3} onClick={onClose}>Close</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    );
}

export default Demo;
