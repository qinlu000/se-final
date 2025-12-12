<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style>
:root {
  /* Palette */
  --c-black: #000000;
  --c-white: #ffffff;
  --c-yellow: #ffe600;
  --c-pink: #ff6b6b;
  --c-cyan: #00f0ff;
  --c-purple: #9d4edd;
  --c-bg: #f3f3f3;

  /* Borders & Shadows */
  --border-thick: 2px solid var(--c-black);
  --border-thin: 1px solid var(--c-black);
  --shadow-hard: 4px 4px 0px var(--c-black);
  --shadow-hover: 2px 2px 0px var(--c-black);
  --radius-s: 4px;
  --radius-m: 8px;
  --radius-full: 999px;
}

page {
  min-height: 100%;
  background-color: var(--c-bg);
  background-image: radial-gradient(#dcdcdc 1px, transparent 1px);
  background-size: 18px 18px;
  color: var(--c-black);
  font-family: 'DM Mono', 'SFMono-Regular', 'Menlo', monospace;
}

.neu-card {
  background: var(--c-white);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  border-radius: var(--radius-m);
}

.neu-btn {
  background: var(--c-yellow);
  border: var(--border-thick);
  box-shadow: var(--shadow-hard);
  border-radius: var(--radius-s);
  color: var(--c-black);
  font-weight: 700;
  transition: transform 0.08s ease, box-shadow 0.08s ease;
}

.neu-btn:active {
  box-shadow: none;
  transform: translate(4px, 4px);
}
</style>
