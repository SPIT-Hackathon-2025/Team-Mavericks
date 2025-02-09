import { Text, useColorModeValue, Box, Grid, Spinner } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import Card from "components/card/Card.js";
import Project from "./Project";
import Project3 from "./Project3";


export default function Projects() {
  // Chakra Color Mode
  const textColorPrimary = useColorModeValue("secondaryGray.900", "white");
  const textColorSecondary = "gray.400";
  const cardShadow = useColorModeValue("0px 18px 40px rgba(112, 144, 176, 0.12)", "unset");

  const [tasks, setTasks] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTasksAndEvents = async () => {
      try {
        const todayResponse = await fetch("http://localhost:8000/today");
        const todayData = await todayResponse.json();
        setTasks(todayData?.tasks || []);

        const date = new Date().toISOString().split("T")[0];
        const eventsResponse = await fetch(`http://localhost:8000/events/${date}`);
        const eventsData = await eventsResponse.json();
        setEvents(eventsData.events || []);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTasksAndEvents();
  }, []);

  return (
    <Card mb={{ base: "0px", "2xl": "20px" }}>
      <Grid templateColumns={{ base: "1fr", md: "1fr 1fr" }} gap={6}>
        {/* First Column: Tasks */}
        <Box>
          <Text color={textColorPrimary} fontWeight="bold" fontSize="2xl" mt="10px" mb="4px">
            Your Tasks
          </Text>
          <Text color={textColorSecondary} fontSize="md" mb="40px">
            Stay on top of your tasks and be productive!
          </Text>
          {loading ? (
            <Spinner />
          ) : tasks.length > 0 ? (
            tasks.map((task, index) => (
              <Project key={index} boxShadow={cardShadow} mb="20px" ranking={index + 1} link="#" task={task} />
            ))
          ) : (
            <Text color={textColorSecondary}>No tasks for today.</Text>
          )}
        </Box>

        {/* Second Column: Events */}
        <Box>
          <Text color={textColorPrimary} fontWeight="bold" fontSize="2xl" mt="10px" mb="4px">
            Your Events
          </Text>
          <Text color={textColorSecondary} fontSize="md" mb="40px">
            Here are your events scheduled for today.
          </Text>
          {loading ? (
            <Spinner />
          ) : events?.primary?.length > 0 ? events.primary.map((event,index) => (
                <Project3 key={index} boxShadow={cardShadow} mb="20px" ranking={index + 1}  event={event} />
              )
          ) : (
            <Text color={textColorSecondary}>No events for today.</Text>
          )}
        </Box>
      </Grid>
    </Card>
  );
}
