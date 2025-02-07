const BASE_URL = "http://localhost:8000";

export interface EndpointType {
  getAll: (skip: number, limit: number) => string;
  getById: (id: string) => string;
  create: string;
  update: (id: string) => string;
  delete: (id: string) => string;
}

export interface EndpointWithGenerate extends EndpointType {
  generate: (...params: string[]) => string;
}

interface EndpointsType {
  data_source: EndpointWithGenerate;
  data_source_columns: EndpointType;
  tasks: EndpointWithGenerate;
  data_source_type: EndpointType;
  requirements: EndpointType;
  script: EndpointType;
}

const createEndpointType = (
  url: string,
  id_field: string = "id"
): EndpointType => {
  const full_url = `${BASE_URL}/${url}`;
  return {
    getAll: (skip: number, limit: number) =>
      `${full_url}/all/?skip=${skip}&limit=${limit}`,
    getById: (id: string) => `${full_url}/?${id_field}=${id}`,
    create: full_url,
    update: (id: string) => `${full_url}/?${id_field}=${id}`,
    delete: (id: string) => `${full_url}/?${id_field}=${id}`,
  };
};
export const endpoints: EndpointsType = {
  data_source: {
    ...createEndpointType("data-sources"),
    generate: () => `${BASE_URL}/data-sources/from-file`,
  },
  data_source_type: createEndpointType("data-source-type"),
  data_source_columns: createEndpointType("data-source-columns"),
  requirements: createEndpointType("requirement"),
  tasks: {
    ...createEndpointType("tasks", "task_id"),
    generate: (id: string) =>
      `${BASE_URL}/tasks/generate/?data_source_id=${id}`,
  },
  script: createEndpointType("script", "data_source_id"),
};
