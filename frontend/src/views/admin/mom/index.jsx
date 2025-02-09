import React, { useEffect, useState } from 'react';
import { Box, Spinner, Text } from "@chakra-ui/react";
import MeetCard from './components/meetingCard';

const Mom = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/mom");
                if (!response.ok) {
                    throw new Error("Failed to fetch data");
                }
                const result = await response.json();
                setData(result);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
        <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
            {loading ? (
                <Spinner size="xl" />
            ) : error ? (
                <Text color="red.500">{error}</Text>
            ) : (
                data && data?.map((item, index) => (
                    <MeetCard key={index} data={item} />
                ))
            )}
        </Box>
    );
};

export default Mom;
