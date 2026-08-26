

export async function toggle_resto_pin(restoId, button) {
  const response = await fetch(`/restaurants/${restoId}/pin`, {
      method: "POST"
  });

  const isPinned = await response.json()

  pinButton.setAttribute(
    "aria-pressed",
    String(isPinned)  
  );
}