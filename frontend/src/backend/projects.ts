import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import axios from 'axios'
import { useCSRF } from '@/backend/security'
import type { Project, Site } from '@/backend/interfaces'
import type { RouteLocationNormalized } from 'vue-router'
import { computed } from 'vue'

export function useUpdateProject(route: RouteLocationNormalized) {
  const { data: csrf } = useCSRF()
  const client = useQueryClient()
  return useMutation({
    mutationFn: (data: Project) =>
      axios.post(`/api/project/${route.params.proj || data.name}/update/`, data, {
        headers: {
          'X-CSRFToken': csrf.value,
        },
      }),
    onSuccess() {
      client.invalidateQueries({ queryKey: ['projects'] })
    },
  })
}

export function useProjectList() {
  return useQuery({
    queryKey: ['projects'],
    queryFn: () =>
      axios.get<Project[]>(`/api/project/list/`).then(res => res.data),
  })
}

export function useProjectDetails(route: RouteLocationNormalized) {
  return useQuery({
    queryKey: ['projectDetails', computed(() => route.params.proj)],
    queryFn: () =>
      axios
        .get<Project>(`/api/project/${route.params.proj}/`)
        .then(res => res.data),
  })
}

export function useCreateSite(route: RouteLocationNormalized) {
  const { data: csrf } = useCSRF()
  const client = useQueryClient()
  return useMutation({
    mutationFn: (data: Site) =>
      axios.post(
        `/api/project/${route.params.proj}/create_site/`,
        data,
        {
          headers: {
            'X-CSRFToken': csrf.value,
          },
        },
      ),
    onSuccess() {
      client.invalidateQueries({
        queryKey: ['projects', 'sites', computed(() => route.params.proj)],
      })
    },
  })
}

export function useUpdateSite(route: RouteLocationNormalized, site: string) {
  const { data: csrf } = useCSRF()
  const client = useQueryClient()
  return useMutation({
    mutationFn: (data: Site) =>
      axios.post(
        `/api/project/${route.params.proj}/site/${site}/update/`,
        data,
        {
          headers: {
            'X-CSRFToken': csrf.value,
          },
        },
      ),
    onSuccess() {
      client.invalidateQueries({
        queryKey: ['projects', 'sites', computed(() => route.params.proj)],
      })
    },
  })
}

export function useProjectSites(route: RouteLocationNormalized) {
  return useQuery({
    queryKey: ['projects', 'sites', computed(() => route.params.proj)],
    queryFn: () =>
      axios
        .get<Site[]>(`/api/project/${route.params.proj}/sites/`)
        .then(res => res.data),
  })
}

export function useProjectSiteCommodities(
  route: RouteLocationNormalized,
  site: string,
) {
  return useQuery({
    queryKey: [
      'projects',
      'commodities',
      computed(() => route.params.proj),
      site,
    ],
    queryFn: () =>
      axios
        .get<
          Site[]
        >(`/api/project/${route.params.proj}/site/${site}/commodities`)
        .then(res => res.data),
  })
}
