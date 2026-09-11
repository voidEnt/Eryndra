# MAP-001 Asset Pass 02 - Validation

**Outcome:** PASS
**Checks:** 81/81 passed

The approved generated master was retained and resized to the exact map canvas. Runtime PNG dimensions, alpha channels, ring-state ordering, black-fracture mask, collision flags, OGG codec/sample rate/channel count/duration, and manifest coverage were checked.

Inter-tone silence was synthesized as two equal 0.65-second intervals. Runtime playback and subjective mix level remain integration checks for RPG Maker MZ.

- PASS - `image-integrity:assets/img/parallaxes/MAP001_WatcherStation_Base.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/pictures/MAP001_Dust_Tremor.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/pictures/MAP001_Ring_Propagated.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/pictures/MAP001_Ring_Pulse.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/pictures/MAP001_Ring_Residual.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/pictures/SYS_Eryndra_Title.png`: verify and full decode succeeded
- PASS - `image-integrity:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: verify and full decode succeeded
- PASS - `image-integrity:review/ChamberCamera_Dormant_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/ChamberCamera_Dust_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/RingCamera_Dormant_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/RingCamera_Dust_tremor_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/RingCamera_Propagated_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/RingCamera_Pulse_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/RingCamera_Residual_816x624.jpg`: verify and full decode succeeded
- PASS - `image-integrity:review/Ring_States_ContactSheet_1632x1248.jpg`: verify and full decode succeeded
- PASS - `exists:assets/img/parallaxes/MAP001_WatcherStation_Base.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/parallaxes/MAP001_WatcherStation_Base.png
- PASS - `size:assets/img/parallaxes/MAP001_WatcherStation_Base.png`: observed=(1392, 1008), expected=(1392, 1008)
- PASS - `mode:assets/img/parallaxes/MAP001_WatcherStation_Base.png`: observed=P, expected=P
- PASS - `exists:assets/img/pictures/MAP001_Ring_Pulse.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/pictures/MAP001_Ring_Pulse.png
- PASS - `size:assets/img/pictures/MAP001_Ring_Pulse.png`: observed=(816, 624), expected=(816, 624)
- PASS - `mode:assets/img/pictures/MAP001_Ring_Pulse.png`: observed=RGBA, expected=RGBA
- PASS - `alpha:assets/img/pictures/MAP001_Ring_Pulse.png`: alpha_range=(0, 208)
- PASS - `exists:assets/img/pictures/MAP001_Ring_Residual.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/pictures/MAP001_Ring_Residual.png
- PASS - `size:assets/img/pictures/MAP001_Ring_Residual.png`: observed=(816, 624), expected=(816, 624)
- PASS - `mode:assets/img/pictures/MAP001_Ring_Residual.png`: observed=RGBA, expected=RGBA
- PASS - `alpha:assets/img/pictures/MAP001_Ring_Residual.png`: alpha_range=(0, 136)
- PASS - `exists:assets/img/pictures/MAP001_Ring_Propagated.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/pictures/MAP001_Ring_Propagated.png
- PASS - `size:assets/img/pictures/MAP001_Ring_Propagated.png`: observed=(816, 624), expected=(816, 624)
- PASS - `mode:assets/img/pictures/MAP001_Ring_Propagated.png`: observed=RGBA, expected=RGBA
- PASS - `alpha:assets/img/pictures/MAP001_Ring_Propagated.png`: alpha_range=(0, 168)
- PASS - `exists:assets/img/pictures/MAP001_Dust_Tremor.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/pictures/MAP001_Dust_Tremor.png
- PASS - `size:assets/img/pictures/MAP001_Dust_Tremor.png`: observed=(816, 624), expected=(816, 624)
- PASS - `mode:assets/img/pictures/MAP001_Dust_Tremor.png`: observed=RGBA, expected=RGBA
- PASS - `alpha:assets/img/pictures/MAP001_Dust_Tremor.png`: alpha_range=(0, 89)
- PASS - `exists:assets/img/pictures/SYS_Eryndra_Title.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/pictures/SYS_Eryndra_Title.png
- PASS - `size:assets/img/pictures/SYS_Eryndra_Title.png`: observed=(816, 624), expected=(816, 624)
- PASS - `mode:assets/img/pictures/SYS_Eryndra_Title.png`: observed=RGBA, expected=RGBA
- PASS - `alpha:assets/img/pictures/SYS_Eryndra_Title.png`: alpha_range=(0, 244)
- PASS - `exists:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/assets/img/tilesets/Eryndra_CinematicCollision_A5.png
- PASS - `size:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: observed=(768, 768), expected=(768, 768)
- PASS - `mode:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: observed=RGBA, expected=RGBA
- PASS - `transparent:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: alpha_range=(0, 0)
- PASS - `ring-state-order`: pulse alpha > propagated alpha > residual alpha
- PASS - `fracture-unlit:Pulse`: max_fracture_alpha=0
- PASS - `fracture-unlit:Residual`: max_fracture_alpha=0
- PASS - `fracture-unlit:Propagated`: max_fracture_alpha=0
- PASS - `tileset-id`: id=7
- PASS - `tile-1536-blocked`: flag=15
- PASS - `tile-1537-passable`: flag=0
- PASS - `unused-star-skip`: all flags except 1536/1537 equal 16
- PASS - `audio-codec`: codec=vorbis
- PASS - `audio-sample-rate`: rate=48000
- PASS - `audio-mono`: channels=1
- PASS - `audio-duration`: duration=3.400000s
- PASS - `manifest-exists`: /workspace/scratch/97aa0d2024e9/Eryndra/work/mapping/MAP-001/pass-02/ASSET_MANIFEST.json
- PASS - `manifest-assets`: asset_records=9
- PASS - `manifest-review-artifacts`: review_records=8
- PASS - `review-cyan-preserved:pulse`: cyan_pixels=6108
- PASS - `review-cyan-preserved:contact-sheet`: cyan_pixels=9554
- PASS - `ring-fits-camera:ring`: ring=[617, 214, 765, 346], camera=[288, 96, 1103, 719]
- PASS - `ring-fits-camera:chamber`: ring=[617, 214, 765, 346], camera=[288, 192, 1103, 815]
- PASS - `manifest-hash:source/MAP001_CanonCorrected_CameraFit.jpg`: observed=e53150f3345cf16958cf97500ab83827f26e83e9df359182ef5719c687bdf2fb, expected=e53150f3345cf16958cf97500ab83827f26e83e9df359182ef5719c687bdf2fb
- PASS - `manifest-hash:assets/img/parallaxes/MAP001_WatcherStation_Base.png`: observed=4fb64a66a9beabf1994f71abe526c1b3b2c3a59fb11435a57ee8a3f4ae9693f1, expected=4fb64a66a9beabf1994f71abe526c1b3b2c3a59fb11435a57ee8a3f4ae9693f1
- PASS - `manifest-hash:assets/img/pictures/MAP001_Ring_Pulse.png`: observed=211e5d3b236d0437f5a2ceac8fff93b28a33f8a234d4b272e3218567e64595c7, expected=211e5d3b236d0437f5a2ceac8fff93b28a33f8a234d4b272e3218567e64595c7
- PASS - `manifest-hash:assets/img/pictures/MAP001_Ring_Residual.png`: observed=fecb3d4f695bb3c5bce8efd3a02ea05d29e974a102551a2fd5e1340eb2d05de7, expected=fecb3d4f695bb3c5bce8efd3a02ea05d29e974a102551a2fd5e1340eb2d05de7
- PASS - `manifest-hash:assets/img/pictures/MAP001_Ring_Propagated.png`: observed=5f082c2c73e73000f9a15319fd781c155d7b36241fb1c8a82c47a1d73a32d5be, expected=5f082c2c73e73000f9a15319fd781c155d7b36241fb1c8a82c47a1d73a32d5be
- PASS - `manifest-hash:assets/img/pictures/MAP001_Dust_Tremor.png`: observed=6255168f89c670184446e4d8dd39b7470a25d2e233fa78adba07e7e3189dcb3a, expected=6255168f89c670184446e4d8dd39b7470a25d2e233fa78adba07e7e3189dcb3a
- PASS - `manifest-hash:assets/img/pictures/SYS_Eryndra_Title.png`: observed=837ccffafe8cc39339249f6ba8e92dd83ac85b0e3710b9ce46436638eaa6b63c, expected=837ccffafe8cc39339249f6ba8e92dd83ac85b0e3710b9ce46436638eaa6b63c
- PASS - `manifest-hash:assets/img/tilesets/Eryndra_CinematicCollision_A5.png`: observed=9542a32e82323eb002e9f3da746fc00f58f3553c6bb31cdf73ccb1253755c7e0, expected=9542a32e82323eb002e9f3da746fc00f58f3553c6bb31cdf73ccb1253755c7e0
- PASS - `manifest-hash:assets/data/Tileset007.fragment.json`: observed=7fa7be8cf7a939cff0ba0a81381ddf540d420c14d6aea70cf4aedd661351301c, expected=7fa7be8cf7a939cff0ba0a81381ddf540d420c14d6aea70cf4aedd661351301c
- PASS - `manifest-hash:assets/audio/se/Ancient_ThreeNote_Resonance.ogg`: observed=8a55c42597e2db818e81d111d4d8e6da76115213402b1af29f298a2696c47faa, expected=8a55c42597e2db818e81d111d4d8e6da76115213402b1af29f298a2696c47faa
- PASS - `manifest-hash:review/ChamberCamera_Dormant_816x624.jpg`: observed=8f8e4a9f1ac4a5ef359374afff67c3d9453ea0e65cf9a287ca61177dc5b5fcbe, expected=8f8e4a9f1ac4a5ef359374afff67c3d9453ea0e65cf9a287ca61177dc5b5fcbe
- PASS - `manifest-hash:review/ChamberCamera_Dust_816x624.jpg`: observed=f1be07b5c3f6744b5c13c40e8466e983f6cbae37b176c367d147c8876e85ac4d, expected=f1be07b5c3f6744b5c13c40e8466e983f6cbae37b176c367d147c8876e85ac4d
- PASS - `manifest-hash:review/RingCamera_Dormant_816x624.jpg`: observed=3e1415b96af7ebdde049251f61b254256192b5a1da3dd27bf97f0ac7dbb62048, expected=3e1415b96af7ebdde049251f61b254256192b5a1da3dd27bf97f0ac7dbb62048
- PASS - `manifest-hash:review/RingCamera_Dust_tremor_816x624.jpg`: observed=eaad79b70f9e43278675ee917765790f48b6df3ad46e42d6395accdf7690cd56, expected=eaad79b70f9e43278675ee917765790f48b6df3ad46e42d6395accdf7690cd56
- PASS - `manifest-hash:review/RingCamera_Propagated_816x624.jpg`: observed=e516b62b5f1c7340f27b766be86aca6db011b7435d1d4069c5d7eb6a81441b8d, expected=e516b62b5f1c7340f27b766be86aca6db011b7435d1d4069c5d7eb6a81441b8d
- PASS - `manifest-hash:review/RingCamera_Pulse_816x624.jpg`: observed=2174b2b8431fdff53b0d8f15b37fbc8ba77dd7318d8d12c27746152579e6e259, expected=2174b2b8431fdff53b0d8f15b37fbc8ba77dd7318d8d12c27746152579e6e259
- PASS - `manifest-hash:review/RingCamera_Residual_816x624.jpg`: observed=84c87f6e592b43e3cc357c1ef0b8cbfdc4f7a887344929be138b6c8294594a7d, expected=84c87f6e592b43e3cc357c1ef0b8cbfdc4f7a887344929be138b6c8294594a7d
- PASS - `manifest-hash:review/Ring_States_ContactSheet_1632x1248.jpg`: observed=df5d6e710db6583a4335e667136c14a45d836ad56eb9586e7f26b71a5501e0f3, expected=df5d6e710db6583a4335e667136c14a45d836ad56eb9586e7f26b71a5501e0f3
- PASS - `no-atomic-temporaries`: none
- PASS - `git-package-file-ceiling`: all files <= 716800 bytes
