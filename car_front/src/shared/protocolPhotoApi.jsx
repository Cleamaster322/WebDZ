import api from "./api.jsx";

export const getProtocolPhotos = async (protocolId) => {
    const response = await api.get(`/cars/protocols/${protocolId}/photos/`);
    return response.data;
};

export const uploadProtocolPhoto = async (protocolId, file, photoType, sortOrder = 0) => {
    const formData = new FormData();

    formData.append("photo_type", photoType);
    formData.append("sort_order", String(sortOrder));
    formData.append("file", file);

    const response = await api.post(
        `/cars/protocols/${protocolId}/photos/create/`,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};

export const updateProtocolPhoto = async (photoId, { file, photoType, sortOrder }) => {
    const formData = new FormData();

    if (photoType) {
        formData.append("photo_type", photoType);
    }

    if (sortOrder !== undefined && sortOrder !== null) {
        formData.append("sort_order", String(sortOrder));
    }

    if (file) {
        formData.append("file", file);
    }

    const response = await api.patch(
        `/cars/protocol-photos/${photoId}/update/`,
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};

export const deleteProtocolPhoto = async (photoId) => {
    await api.delete(`/cars/protocol-photos/${photoId}/delete/`);
};