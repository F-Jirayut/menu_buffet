export function decodePayloadToken(token) {
    if (!token) return null
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return payload
    } catch (e) {
      console.error('Invalid JWT', e)
      return null
    }
  }