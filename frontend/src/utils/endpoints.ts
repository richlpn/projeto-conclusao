const BASE_URL = "http://localhost:8000";

export interface EndpointType {
  getAll: (skip: number, limit: number) => string;
  getById: (id: string) => string;
  create: string;
  update: (id: string) => string;
  delete: (id: string) => string;
}

export interface EndpointWithFile extends EndpointType {
  file: string;
}

interface EndpointsType {
  data_source: EndpointWithFile;
  data_source_columns: EndpointType;
  tasks: EndpointType;
  data_source_type: EndpointType;
  requirements: EndpointType;
}

const createEndpointType = (url: string): EndpointType => {
  const full_url = `${BASE_URL}/${url}`;
  return {
    getAll: (skip: number, limit: number) =>
      `${full_url}/all/?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${full_url}/?id=${id}`,
    create: full_url,
    update: (id: string) => `${full_url}/?id=${id}`,
    delete: (id: string) => `${full_url}/?id=${id}`,
  };
};
export const endpoints: EndpointsType = {
  data_source: {
    ...createEndpointType("data-sources"),
    file: `${BASE_URL}/data-sources/from-file`,
  },
  data_source_type: createEndpointType("data-source-type"),
  data_source_columns: createEndpointType("data-source-columns"),
  requirements: createEndpointType("requirement"),
  tasks: createEndpointType("task"),
};
