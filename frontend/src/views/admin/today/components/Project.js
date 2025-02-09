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
  const { task, ...rest } = props;
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
            {task?.properties?.Task?.title?.[0]?.text?.content || "No Title"}
          </Text>
          <Text fontWeight="500" color={textColorSecondary} fontSize="sm" me="4px">
            {task?.properties["Due Date"]?.date?.start || "No Due Date"}{" "}
            <Link fontWeight="500" color={brandColor} href={`mailto:${task?.properties?.Assignee?.people?.[0]?.person?.email}`} fontSize="sm">
              {task?.properties?.Assignee?.people?.[0]?.person?.email || "No Assignee"}
            </Link>
          </Text>
        </Box>
        <Link href="#" variant="no-hover" me="16px" ms="auto" p="0px !important" onClick={handleSeeDetails}>
          <Icon as={MdExpand} color="secondaryGray.500" h="18px" w="18px" />
        </Link>
      </Flex>
      {showBody && (
        <Text>
          {task?.properties?.Description?.rich_text?.[0]?.text?.content || "No Description"}
        </Text>
      )}
    </Card>
  );
}
