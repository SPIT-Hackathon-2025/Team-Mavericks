import React from "react";

// Chakra imports
import { Flex, Heading, useColorModeValue } from "@chakra-ui/react";

// Custom components
import { HorizonLogo } from "components/icons/Icons";
import { HSeparator } from "components/separator/Separator";
import { RiRobot3Fill } from "react-icons/ri";


export function SidebarBrand() {
  //   Chakra color mode
  let logoColor = useColorModeValue("navy.700", "white");

  return (
    <Flex align='center' direction='column'>
      {/* <HorizonLogo h='26px' w='175px' my='32px' color={logoColor} /> */}
      <Heading size="xl" display="inline-flex" alignItems="center" gap={2}>
        <RiRobot3Fill />
        SyncUp
      </Heading>      <HSeparator mb='20px' />
    </Flex>
  );
}

export default SidebarBrand;
