import {
    Button,
    Container,
    Flex,
    Heading,
    SkeletonText,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useEffect } from "react";
import { z } from "zod";

import { PlansService } from "../../client";
import ActionsMenu from "../../components/Common/ActionsMenu";
import Navbar from "../../components/Common/Navbar";
import AddPlan from "../../components/Plans/AddPlan";

const plansSearchSchema = z.object({
    page: z.number().catch(1),
});

export const Route = createFileRoute("/_layout/plans")({
    component: Plans,
    validateSearch: (search) => plansSearchSchema.parse(search),
});

const PER_PAGE = 5;

function getPlansQueryOptions({ page }: { page: number }) {
    return {
        queryFn: () => PlansService.readPlans({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
        queryKey: ["plans", { page }],
    };
}

function PlansTable() {
    const queryClient = useQueryClient();
    const { page } = Route.useSearch();
    const navigate = useNavigate({ from: Route.fullPath });
    const setPage = (page: number) => navigate({ search: (prev) => ({ ...prev, page }) });

    const { data: plansData, isPending, isPlaceholderData, error } = useQuery({
        ...getPlansQueryOptions({ page }),
        placeholderData: (prevData) => prevData,
    });

    console.log("Full plansData - :", plansData);

    const plans = plansData;
    console.log("Extracted plans - :", plans);

    const hasNextPage = !isPlaceholderData && plans?.length === PER_PAGE;
    const hasPreviousPage = page > 1;

    useEffect(() => {
        if (hasNextPage) {
            queryClient.prefetchQuery(getPlansQueryOptions({ page: page + 1 }));
        }
    }, [page, queryClient, hasNextPage]);

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <>
            <TableContainer>
                <Table size={{ base: "sm", md: "md" }}>
                    <Thead>
                        <Tr>
                            <Th>ID</Th>
                            <Th>Name</Th>
                            <Th>Description</Th>
                            <Th>Actions</Th>
                        </Tr>
                    </Thead>
                    {isPending ? (
                        <Tbody>
                            <Tr>
                                {new Array(4).fill(null).map((_, index) => (
                                    <Td key={index}>
                                        <SkeletonText noOfLines={1} paddingBlock="16px" />
                                    </Td>
                                ))}
                            </Tr>
                        </Tbody>
                    ) : (
                        <Tbody>
                            {plans?.map((plan) => (
                                <Tr key={plan.id} opacity={isPlaceholderData ? 0.5 : 1}>
                                    <Td>{plan.id}</Td>
                                    <Td isTruncated maxWidth="150px">
                                        {plan.nombre}
                                    </Td>
                                    <Td
                                        color={!plan.descripcion ? "ui.dim" : "inherit"}
                                        isTruncated
                                        maxWidth="150px"
                                    >
                                        {plan.descripcion ?? "N/A"}
                                    </Td>
                                    <Td>
                                        <ActionsMenu type={"Plan"} value={plan} />
                                    </Td>
                                </Tr>
                            ))}
                        </Tbody>
                    )}
                </Table>
            </TableContainer>
            <Flex
                gap={4}
                alignItems="center"
                mt={4}
                direction="row"
                justifyContent="flex-end"
            >
                <Button onClick={() => setPage(page - 1)} isDisabled={!hasPreviousPage}>
                    Previous
                </Button>
                <span>Page {page}</span>
                <Button isDisabled={!hasNextPage} onClick={() => setPage(page + 1)}>
                    Next
                </Button>
            </Flex>
        </>
    );
}

function Plans() {
    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
                Plans Management
            </Heading>

            <Navbar type={"Plan"} addModalAs={AddPlan} />
            <PlansTable />
        </Container>
    );
}

export default Plans;
