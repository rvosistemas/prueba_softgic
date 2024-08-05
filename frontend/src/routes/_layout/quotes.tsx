import {
    Button,
    Container,
    Flex,
    Heading,
    Input,
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
import { useEffect, useState, useMemo } from "react";
import { z } from "zod";

import { QuotesService, QuotePublic } from "../../client";

const quotesSearchSchema = z.object({
    page: z.number().catch(1),
});

export const Route = createFileRoute("/_layout/quotes")({
    component: Quotes,
    validateSearch: (search) => quotesSearchSchema.parse(search),
});

const PER_PAGE = 5;

function getQuotesQueryOptions({ page }: { page: number }) {
    return {
        queryFn: () => QuotesService.getQuotes({
            page,
            limit: PER_PAGE,
            sortColumn: '',
            sortOrder: '',
            filters: { amount: '', date: '' },
        }),
        queryKey: ["quotes", { page }],
    };
}

function QuotesTable() {
    const queryClient = useQueryClient();
    const { page } = Route.useSearch();
    const navigate = useNavigate({ from: Route.fullPath });
    const setPage = (page: number) => navigate({ search: (prev) => ({ ...prev, page }) });

    const [sortColumn, setSortColumn] = useState<string>('id');
    const [sortOrder, setSortOrder] = useState<string>('asc');
    const [search, setSearch] = useState<string>('');

    const { data: quotesData, isPending, isPlaceholderData, error } = useQuery({
        ...getQuotesQueryOptions({ page }),
        placeholderData: (prevData) => prevData,
    });

    const handleSort = (column: string) => {
        const order = sortColumn === column && sortOrder === 'asc' ? 'desc' : 'asc';
        setSortColumn(column);
        setSortOrder(order);
    };

    const handleSearch = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearch(event.target.value);
    };

    const filteredQuotes = useMemo(() => {
        if (!quotesData) return [];
        return quotesData.filter((quote: QuotePublic) =>
            quote.response_body.suc_nombre.toLowerCase().includes(search.toLowerCase())
        );
    }, [quotesData, search]);

    const sortedQuotes = useMemo(() => {
        const sorted = [...filteredQuotes];
        sorted.sort((a, b) => {
            const aValue = a.response_body.cotizaciones[0] as unknown as Record<string, any>;
            const bValue = b.response_body.cotizaciones[0] as unknown as Record<string, any>;
            if (aValue[sortColumn] < bValue[sortColumn]) return sortOrder === 'asc' ? -1 : 1;
            if (aValue[sortColumn] > bValue[sortColumn]) return sortOrder === 'asc' ? 1 : -1;
            return 0;
        });
        return sorted;
    }, [filteredQuotes, sortColumn, sortOrder]);

    const paginatedQuotes = sortedQuotes.slice((page - 1) * PER_PAGE, page * PER_PAGE);

    const hasNextPage = quotesData && (page * PER_PAGE) < quotesData.length;
    const hasPreviousPage = page > 1;

    useEffect(() => {
        if (hasNextPage) {
            queryClient.prefetchQuery(getQuotesQueryOptions({ page: page + 1 }));
        }
    }, [page, queryClient, hasNextPage]);

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <>
            <Flex mb={4}>
                <Input
                    placeholder="Buscar por Sucursal"
                    value={search}
                    onChange={handleSearch}
                />
            </Flex>
            <TableContainer>
                <Table size={{ base: "sm", md: "md" }}>
                    <Thead>
                        <Tr>
                            <Th onClick={() => handleSort('id')}>ID</Th>
                            <Th onClick={() => handleSort('sum_aseg_4')}>Amount</Th>
                            <Th onClick={() => handleSort('ini_vig_reportada')}>Date</Th>
                            <Th>Sucursal</Th>
                            <Th>Distribuidor</Th>
                        </Tr>
                    </Thead>
                    {isPending ? (
                        <Tbody>
                            <Tr>
                                {new Array(5).fill(null).map((_, index) => (
                                    <Td key={index}>
                                        <SkeletonText noOfLines={1} paddingBlock="16px" />
                                    </Td>
                                ))}
                            </Tr>
                        </Tbody>
                    ) : (
                        <Tbody>
                            {paginatedQuotes.map((quote) => (
                                <Tr key={quote.response_body.cotizaciones[0].id} opacity={isPlaceholderData ? 0.5 : 1}>
                                    <Td>{quote.response_body.cotizaciones[0].id}</Td>
                                    <Td>{quote.response_body.cotizaciones[0].det_solicitudes[0].sum_aseg_4}</Td>
                                    <Td>{quote.response_body.cotizaciones[0].det_solicitudes[0].ini_vig_reportada}</Td>
                                    <Td>{quote.response_body.suc_nombre}</Td>
                                    <Td>{quote.response_body.distribuidor_nombre}</Td>
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

function Quotes() {
    return (
        <Container maxW="full">
            <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
                Quotes Management
            </Heading>
            <QuotesTable />
        </Container>
    );
}

export default Quotes;
