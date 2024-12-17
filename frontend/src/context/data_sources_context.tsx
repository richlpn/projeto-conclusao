import { useFetchAllData } from "@/hooks/useFetchAllData";
import { dataSourceSchema, DataSourceSchema } from "@/types/data_source.type";
import { endpoints } from "@/utils/endpoints";
import React from "react";

interface DataSourceContextType {
  dataSources: DataSourceSchema[] | undefined;
  isLoading: boolean;
  error: Error | null;
  refetch: () => void;
}
const DataSourceContext = React.createContext<
  DataSourceContextType | undefined
>(undefined);

export const DataSourceProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const { data, isLoading, error, refetch } = useFetchAllData(
    dataSourceSchema,
    endpoints.data_source.getAll(0, 100)
  );

  const value = React.useMemo(
    () => ({
      dataSources: data,
      isLoading,
      error,
      refetch,
    }),
    [data, isLoading, error, refetch]
  );

  return (
    <DataSourceContext.Provider value={value}>
      {children}
    </DataSourceContext.Provider>
  );
};

export const useDataSources = () => {
  const context = React.useContext(DataSourceContext);
  if (context === undefined) {
    throw new Error("useDataSources must be used within a DataSourceProvider");
  }
  return context;
};
