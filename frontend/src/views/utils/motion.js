import { ref, h } from 'vue'

export default {
  name: 'Motion',
  props: {
    delay: {
      type: Number,
      default: 0
    }
  },
  setup(props, { slots }) {
    const show = ref(false)
    
    setTimeout(() => {
      show.value = true
    }, props.delay)
    
    return () => {
      if (show.value) {
        return slots.default ? slots.default() : null
      }
      return null
    }
  }
}
