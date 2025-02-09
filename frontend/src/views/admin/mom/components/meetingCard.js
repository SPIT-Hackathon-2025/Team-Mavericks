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
    useDisclosure,
    Divider,
    Box,
    List,
    ListItem,
    ListIcon
} from "@chakra-ui/react";
import { MdAccessTime, MdLocationOn, MdCheckCircle, MdEmail } from "react-icons/md";
import { useColorModeValue } from "@chakra-ui/react";

const Demo = ({ data }) => {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const textColorPrimary = useColorModeValue("secondaryGray.900", "white");

    const handleMailMom = async () => {
        try {
            const response = await fetch(`http://localhost:8000/mail-mom/${data.title}`);
            if (!response.ok) {
                throw new Error("Failed to send transcript email");
            }
            const result = await response.json();
            alert(result.success || result.error);
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while sending the email.");
        }
    };


    return (
        <>
            {/* Meeting Card */}
            <Card width="350px" boxShadow="lg" borderRadius="lg" p={4}>
                <CardHeader>
                    <Stack direction="row" align="center" spacing={3}>
                        <Avatar name="Nue Camp" src="https://picsum.photos/200/300" size="md" />
                        <Text color={textColorPrimary} fontWeight='bold' fontSize='2xl'>
                            {data.title}
                        </Text>
                    </Stack>
                </CardHeader>

                {/* Meeting Details */}
                <CardBody>
                    <Stack spacing={3}>
                        <Flex align="center" gap={2}>
                            <Icon as={MdAccessTime} color="blue.500" />
                            <Text fontSize="sm" color={textColorPrimary}>{data.time}</Text>
                        </Flex>
                        <Flex align="center" gap={2}>
                            <Icon as={MdLocationOn} color="red.500" />
                            <Text fontSize="sm" color={textColorPrimary}>Google Meet</Text>
                        </Flex>
                    </Stack>
                </CardBody>

                {/* Footer with Action Button */}
                <CardFooter display="flex" justifyContent="flex-end">
                    <Button variant="outline" colorScheme="blue" onClick={onOpen}>View</Button>
                </CardFooter>
            </Card>

            {/* Detailed Meeting Modal */}
            <Modal isOpen={isOpen} onClose={onClose} size="xl">
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>Minutes of Meeting</ModalHeader>
                    <ModalBody>
                        <Stack spacing={4}>
                            {/* Agenda Section */}
                            <Box>
                                <Heading size="md">📌 Agenda</Heading>
                                <List spacing={2} mt={2}>
                                    {data.agenda.map((point, index) => (
                                        <ListItem key={index}>
                                            <ListIcon as={MdCheckCircle} color="green.500" />
                                            {point}
                                        </ListItem>
                                    ))}
                                </List>
                            </Box>

                            <Divider />

                            {/* Minutes Section */}
                            <Box>
                                <Heading size="md">📝 Minutes</Heading>
                                {data.minutes.map((minute, index) => (
                                    <Box key={index} p={3} border="1px solid" borderRadius="md" borderColor="gray.300">
                                        <Text fontWeight="bold">🔹 {minute.agenda_point}</Text>
                                        <Text color="gray.600">{minute.discussion}</Text>
                                        <Text fontWeight="bold" mt={2}>🔹 Action Items:</Text>
                                        <List spacing={1}>
                                            {minute.action_items.map((item, i) => (
                                                <ListItem key={i} ml={4}>
                                                    ✅ {item.item} - <b>{item.assigned_to}</b> (Deadline: {item.deadline})
                                                </ListItem>
                                            ))}
                                        </List>
                                    </Box>
                                ))}
                            </Box>

                            <Divider />

                            {/* Decisions Made */}
                            <Box>
                                <Heading size="md">✅ Decisions Made</Heading>
                                <List spacing={2} mt={2}>
                                    {data["descision made"].map((decision, index) => (
                                        <ListItem key={index}>
                                            <ListIcon as={MdCheckCircle} color="green.500" />
                                            {decision}
                                        </ListItem>
                                    ))}
                                </List>
                            </Box>

                            <Divider />

                            {/* Next Meeting Details */}
                            <Box>
                                <Heading size="md">📅 Next Meeting</Heading>
                                <Text>
                                    Date: {data["next meeting"].date || "Not scheduled yet"} <br />
                                    Time: {data["next meeting"].time || "Not specified"} <br />
                                    Location: {data["next meeting"].location || "TBD"}
                                </Text>
                            </Box>

                            <Divider />

                            {/* Adjournment Time */}
                            <Box>
                                <Heading size="md">⏳ Adjournment</Heading>
                                <Text>Meeting ended at: {data.adjournment["Time of Adjournment"]}</Text>
                            </Box>

                            <Divider />

                            {/* Additional Notes */}
                            <Box>
                                <Heading size="md">📝 Additional Notes</Heading>
                                <Text>{data["additional notes"]}</Text>
                            </Box>

                            <Divider />

                            {/* Response Message */}
                            <Box>
                                <Heading size="md">📩 Response</Heading>
                                <Text whiteSpace="pre-line">{data.response.response}</Text>
                            </Box>
                        </Stack>
                    </ModalBody>

                    <ModalFooter>
                        <Button leftIcon={<MdEmail />} colorScheme="blue" mr={3} onClick={handleMailMom}>
                            Mail MoM to Me
                        </Button>
                        <Button leftIcon={<MdEmail />} colorScheme="green">
                            Mail MoM to Attendees
                        </Button>
                        <Button variant="ghost" onClick={onClose}>Close</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    );
};

export default Demo;
