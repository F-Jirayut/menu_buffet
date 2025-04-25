import { useAuthStore } from '@/stores/authStore'

export const authMiddleware = async (to, from, next) => {
  const auth = useAuthStore()
  const token = auth.access_token

  const isTokenExpired = () => {
    if (!token) return true
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload.exp < Math.floor(Date.now() / 1000)
    } catch (e) {
      return true
    }
  }

  if (!token || isTokenExpired()) {
    await auth.logout()
    if (to.name !== 'Login') {
      return next({ name: 'Login' })
    } else {
      return next()
    }
  }
  

  if (to.name === 'Login' && token) {
    return next({ name: 'Dashboard' })
  }

  await auth.fetchProfile()

  const userPermissions = new Set(auth.user?.permissions || [])
  const metaPermissions = to.meta?.permissions

  let requiredPermissions = []

  if (Array.isArray(metaPermissions)) {
    requiredPermissions = metaPermissions
  } else if (typeof metaPermissions === 'object' && metaPermissions !== null) {
    const hasId = Boolean(to.params?.id)
    if (hasId && metaPermissions.update) {
      requiredPermissions.push(metaPermissions.update)
    } else if (!hasId && metaPermissions.create) {
      requiredPermissions.push(metaPermissions.create)
    }
  }

  const hasAllPermissions = requiredPermissions.every(permission =>
    userPermissions.has(permission)
  )

  if (requiredPermissions.length > 0 && !hasAllPermissions) {
    return next({ path: '/404' })
  }

  return next()
}

