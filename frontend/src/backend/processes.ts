import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import type { Process, Site } from '@/backend/interfaces'
import type { RouteLocationNormalized } from 'vue-router'
import { computed } from 'vue'
import { useCSRF } from '@/backend/security'

export function useDefProcesses() {
  return useQuery({
    queryKey: ['defProcesses'],
    queryFn: () =>
      axios
        .get<Process[]>(`/api/def_processes/`)
        .then(response => response.data),
  })
}

export function useProcesses(route: RouteLocationNormalized, site: Site) {
  return useQuery({
    queryKey: ['processes', computed(() => route.params.proj), site.name],
    queryFn: () =>
      axios
        .get<
          Process[]
        >(`/api/project/${route.params.proj}/site/${site.name}/processes`)
        .then(response => response.data),
  })
}

export function useAddDefProcess(route: RouteLocationNormalized) {
  const queryClient = useQueryClient()
  const { data: csrf } = useCSRF()
  return useMutation({
    mutationFn: (data: { site_name: string; def_proc_name: string }) =>
      axios.post(
        `/api/project/${route.params.proj}/site/${data.site_name}/def_processes/${data.def_proc_name}/add/`,
        {},
        {
          headers: {
            'X-CSRFToken': csrf.value,
          },
        },
      ),
    onSuccess() {
      queryClient.invalidateQueries({
        queryKey: ['processes', route.params.proj],
      })
    },
  })
}