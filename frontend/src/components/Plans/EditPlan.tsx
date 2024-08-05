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
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { type SubmitHandler, useForm } from "react-hook-form";

import {
    type ApiError,
    type PlanPublic,
    type PlanUpdate,
    PlansService,
} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import { handleError } from "../../utils";

interface EditPlanProps {
    plan: PlanPublic;
    isOpen: boolean;
    onClose: () => void;
}

const EditPlan = ({ plan, isOpen, onClose }: EditPlanProps) => {
    const queryClient = useQueryClient();
    const showToast = useCustomToast();
    const {
        register,
        handleSubmit,
        reset,
        formState: { isSubmitting, errors, isDirty },
    } = useForm<PlanUpdate>({
        mode: "onBlur",
        criteriaMode: "all",
        defaultValues: {
            nombre: plan.nombre,
            descripcion: plan.descripcion,
        },
    });

    const mutation = useMutation({
        mutationFn: (data: PlanUpdate) =>
            PlansService.updatePlan({ id: plan.id, requestBody: data }),
        onSuccess: () => {
            showToast("Success!", "Plan updated successfully.", "success");
            onClose();
        },
        onError: (err: ApiError) => {
            handleError(err, showToast);
        },
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ["plans"] });
        },
    });

    const onSubmit: SubmitHandler<PlanUpdate> = async (data) => {
        mutation.mutate(data);
    };

    const onCancel = () => {
        reset();
        onClose();
    };

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
                    <ModalHeader>Edit Plan</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody pb={6}>
                        <FormControl isInvalid={!!errors.nombre}>
                            <FormLabel htmlFor="nombre">Name</FormLabel>
                            <Input
                                id="nombre"
                                {...register("nombre", {
                                    required: "Name is required",
                                })}
                                type="text"
                            />
                            {errors.nombre && (
                                <FormErrorMessage>{errors.nombre.message}</FormErrorMessage>
                            )}
                        </FormControl>
                        <FormControl mt={4}>
                            <FormLabel htmlFor="descripcion">Description</FormLabel>
                            <Input
                                id="descripcion"
                                {...register("descripcion")}
                                placeholder="Description"
                                type="text"
                            />
                        </FormControl>
                    </ModalBody>
                    <ModalFooter gap={3}>
                        <Button
                            variant="primary"
                            type="submit"
                            isLoading={isSubmitting}
                            isDisabled={!isDirty}
                        >
                            Save
                        </Button>
                        <Button onClick={onCancel}>Cancel</Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>
        </>
    );
};

export default EditPlan;
