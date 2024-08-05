import {
    Button,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Input,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"

import { type ApiError, type PlanCreate, PlansService } from "../../client"
import useCustomToast from "../../hooks/useCustomToast"
import { handleError } from "../../utils"

interface AddPlanProps {
    isOpen: boolean
    onClose: () => void
}

const AddPlan = ({ isOpen, onClose }: AddPlanProps) => {
    const queryClient = useQueryClient()
    const showToast = useCustomToast()
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
    } = useForm<PlanCreate>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            nombre: "",
            descripcion: "",
        },
    })

    const mutation = useMutation({
        mutationFn: (data: PlanCreate) =>
            PlansService.createPlan({ requestBody: data }),
        onSuccess: () => {
            showToast("Success!", "Plan created successfully.", "success")
            reset()
            onClose()
        },
        onError: (err: ApiError) => {
            handleError(err, showToast)
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ["plans"] })
        },
    })

    const onSubmit: SubmitHandler<PlanCreate> = (data) => {
        mutation.mutate({ ...data, activo: true })
    }

    return (
        <>
            <Modal
                isOpen={isOpen}
                onClose={onClose}
                size={{ base: "sm", md: "md" }}
                isCentered
            >
                <ModalOverlay />
                <ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
                    <ModalHeader>Add Plan</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl isRequired isInvalid={!!errors.nombre}>
                            <FormLabel htmlFor="name">Name</FormLabel>
                            <Input
                                id="name"
                                {...register("nombre", {
                                    required: "Name is required.",
                                })}
                                placeholder="Name"
                                type="text"
                            />
                            {errors.nombre && (
                                <FormErrorMessage>{errors.nombre.message}</FormErrorMessage>
                            )}
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor="description">Description</FormLabel>
                            <Input
                                id="description"
                                {...register("descripcion")}
                                placeholder="Description"
                                type="text"
                            />
                        </FormControl>
                    </ModalBody>

                    <ModalFooter gap={3}>
                        <Button variant="primary" type="submit" isLoading={isSubmitting}>
                            Save
                        </Button>
                        <Button onClick={onClose}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    )
}

export default AddPlan
