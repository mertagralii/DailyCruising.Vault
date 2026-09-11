---
rol: map
kapsam: api
guncelleme: 2026-09-12
durum: uretilen
---

# Veritabanı Şeması — GÜNCEL (üretilen)

⚠️ **BU DOSYA ELLE YAZILMAZ.** `araclar/sema-cikar.py` üretir; elle
yapılan değişiklik ilk çalıştırmada kaybolur.

Tasarım gerekçesi burada DEĞİL: neden bir kısıt var, neden bir tablo
böyle bölündü — hepsi [[api-sema]] ve [[api-kararlar]] içinde. Burada
yalnız *bugün veritabanında ne var* yazıyor.

**Ne zaman okunur:** hangi tablo/kolon/kısıt var sorusu.
**Ne zaman yazılır:** her migration uygulandıktan sonra betiği çalıştır.

**88 tablo** (olay günlüğü parçaları hariç).

## `Adverts`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Title` | character varying | hayır |  |
| `Placement` | character varying | hayır |  |
| `FileKey` | character varying | evet |  |
| `TargetUrl` | character varying | hayır |  |
| `StartsAt` | timestamp with time zone | hayır |  |
| `EndsAt` | timestamp with time zone | hayır |  |
| `IsActive` | boolean | hayır |  |
| `SortOrder` | integer | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Adverts_Adres` — `CHECK ((("TargetUrl")::text ~~ 'https://%'::text))`
- `CK_Adverts_Aralik` — `CHECK (("EndsAt" > "StartsAt"))`
- `CK_Adverts_Placement_Enum` — `CHECK ((("Placement")::text = ANY ((ARRAY['HomeHero'::character varying, 'HomeBelowSearch'::character varying, 'SearchResults'::character varying, 'BoatDetail'::character varying, 'BlogSidebar'::character varying])::text[])))`

## `Amenities`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Category` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |

## `AmenityTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `AmenityId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_AmenityTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BlogCategories`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Slug` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |

## `BlogCategoryTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BlogCategoryId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BlogCategoryTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BlogPostTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BlogPostId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Title` | character varying | hayır |  |
| `Summary` | character varying | evet |  |
| `Body` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BlogPostTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BlogPosts`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `AuthorUserId` | uuid | hayır |  |
| `AuthorPartnerId` | uuid | evet |  |
| `BlogCategoryId` | uuid | evet |  |
| `Slug` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `ApprovedByUserId` | uuid | evet |  |
| `ApprovedAt` | timestamp with time zone | evet |  |
| `CoverFileKey` | character varying | evet |  |
| `ViewCount` | integer | hayır |  |
| `PublishedAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `RejectionReason` | character varying | evet |  |

Kısıtlar:

- `CK_BlogPosts_PartnerApproval` — `CHECK ((("AuthorPartnerId" IS NULL) OR (("Status")::text <> 'Published'::text) OR (("ApprovedByUserId" IS NOT NULL) AND ("ApprovedAt" IS NOT NULL))))`
- `CK_BlogPosts_PublishedAt` — `CHECK (((("Status")::text <> 'Published'::text) OR ("PublishedAt" IS NOT NULL)))`
- `CK_BlogPosts_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Draft'::character varying, 'UnderReview'::character varying, 'Published'::character varying, 'Rejected'::character varying])::text[])))`

## `BoardingScans`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `ScannedByUserId` | uuid | hayır |  |
| `ScannedAt` | timestamp with time zone | hayır |  |
| `Method` | character varying | hayır |  |
| `DeviceInfo` | character varying | evet |  |
| `Succeeded` | boolean | hayır |  |
| `FailureReason` | character varying | evet |  |
| `Note` | character varying | evet |  |

Kısıtlar:

- `CK_BoardingScans_Method_Enum` — `CHECK ((("Method")::text = ANY ((ARRAY['Camera'::character varying, 'Keyboard'::character varying, 'Manual'::character varying])::text[])))`

## `BoardingTickets`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `TokenSha256` | character varying | hayır |  |
| `IssuedAt` | timestamp with time zone | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `RevokedAt` | timestamp with time zone | evet |  |
| `TokenEncrypted` | character varying | evet |  |

## `BoatAmenities`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `BoatId` | uuid | hayır |  |
| `AmenityId` | uuid | hayır |  |
| `Inclusion` | character varying | hayır | `'OnBoard'::character varying` |

Kısıtlar:

- `CK_BoatAmenities_Inclusion_Enum` — `CHECK ((("Inclusion")::text = ANY ((ARRAY['OnBoard'::character varying, 'Included'::character varying, 'Extra'::character varying])::text[])))`

## `BoatCrewLanguages`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `BoatId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |

## `BoatDocuments`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `DocumentType` | character varying | hayır |  |
| `FileKey` | character varying | hayır |  |
| `DocumentNumber` | character varying | evet |  |
| `IssuedAt` | timestamp with time zone | evet |  |
| `ExpiresAt` | timestamp with time zone | evet |  |
| `Status` | character varying | hayır |  |
| `VerifiedAt` | timestamp with time zone | evet |  |
| `VerifiedByUserId` | uuid | evet |  |
| `ExpiryNotifiedAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `RejectionReason` | character varying | evet |  |
| `ReviewNote` | character varying | evet |  |

Kısıtlar:

- `CK_BoatDocuments_DocumentType_Enum` — `CHECK ((("DocumentType")::text = ANY ((ARRAY['Registration'::character varying, 'Insurance'::character varying, 'TourismCertificate'::character varying, 'Other'::character varying])::text[])))`
- `CK_BoatDocuments_RedSebebi` — `CHECK ((("RejectionReason" IS NULL) OR (("Status")::text = 'Rejected'::text)))`
- `CK_BoatDocuments_RejectionReason_Enum` — `CHECK ((("RejectionReason" IS NULL) OR (("RejectionReason")::text = ANY ((ARRAY['Unreadable'::character varying, 'Expired'::character varying, 'WrongDocument'::character varying, 'MismatchedInfo'::character varying])::text[]))))`
- `CK_BoatDocuments_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Pending'::character varying, 'Verified'::character varying, 'Rejected'::character varying, 'Expired'::character varying])::text[])))`

## `BoatMedia`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `MediaType` | character varying | hayır |  |
| `FileKey` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsCover` | boolean | hayır |  |
| `Width` | integer | evet |  |
| `Height` | integer | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BoatMedia_MediaType_Enum` — `CHECK ((("MediaType")::text = ANY ((ARRAY['Photo'::character varying, 'Video'::character varying])::text[])))`

## `BoatRentalTypeTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatRentalTypeId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Program` | text | evet |  |
| `Highlights` | text | evet |  |
| `Inclusions` | text | evet |  |
| `Exclusions` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BoatRentalTypeTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BoatRentalTypes`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `RentalTypeId` | uuid | hayır |  |
| `StartTime` | time without time zone | evet |  |
| `EndTime` | time without time zone | evet |  |
| `DurationDays` | integer | evet |  |
| `WeekStartDay` | text | evet |  |
| `ListCurrency` | character varying | hayır |  |
| `InfantMaxAge` | integer | hayır |  |
| `ChildMaxAge` | integer | hayır |  |
| `MinPassengers` | integer | evet |  |
| `IsActive` | boolean | hayır |  |
| `SortOrder` | integer | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `DiverCapacity` | integer | evet |  |
| `MaxNights` | integer | evet |  |
| `MinNights` | integer | evet |  |
| `NonDiverCapacity` | integer | evet |  |

Kısıtlar:

- `CK_BoatRentalTypes_AgeLimits` — `CHECK ((("InfantMaxAge" >= 0) AND ("ChildMaxAge" > "InfantMaxAge")))`
- `CK_BoatRentalTypes_DiverCapacity` — `CHECK (((("DiverCapacity" IS NULL) OR ("DiverCapacity" >= 0)) AND (("NonDiverCapacity" IS NULL) OR ("NonDiverCapacity" >= 0))))`
- `CK_BoatRentalTypes_ListCurrency_Enum` — `CHECK ((("ListCurrency")::text = ANY ((ARRAY['TRY'::character varying, 'USD'::character varying, 'EUR'::character varying, 'GBP'::character varying])::text[])))`
- `CK_BoatRentalTypes_MinPassengers` — `CHECK ((("MinPassengers" IS NULL) OR ("MinPassengers" > 0)))`
- `CK_BoatRentalTypes_NightRange` — `CHECK (((("MinNights" IS NULL) OR ("MinNights" >= 1)) AND (("MaxNights" IS NULL) OR ("MaxNights" >= 1)) AND (("MinNights" IS NULL) OR ("MaxNights" IS NULL) OR ("MinNights" <= "MaxNights"))))`
- `CK_BoatRentalTypes_TimeRange` — `CHECK ((("StartTime" IS NULL) OR ("EndTime" IS NULL) OR ("StartTime" < "EndTime")))`
- `CK_BoatRentalTypes_WeekStartDay_Enum` — `CHECK ((("WeekStartDay" IS NULL) OR ("WeekStartDay" = ANY (ARRAY['Sunday'::text, 'Monday'::text, 'Tuesday'::text, 'Wednesday'::text, 'Thursday'::text, 'Friday'::text, 'Saturday'::text]))))`

## `BoatRules`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `BoatId` | uuid | hayır |  |
| `RuleId` | uuid | hayır |  |
| `IsAllowed` | boolean | hayır |  |
| `Note` | character varying | evet |  |

## `BoatSlugs`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Slug` | character varying | hayır |  |
| `IsCanonical` | boolean | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `BoatTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Description` | text | evet |  |
| `DepartureDescription` | text | evet |  |
| `RulesText` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BoatTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BoatTypeTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatTypeId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_BoatTypeTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `BoatTypes`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |

## `Boats`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `Name` | character varying | hayır |  |
| `Slug` | character varying | hayır |  |
| `BoatTypeId` | uuid | hayır |  |
| `RegionId` | uuid | hayır |  |
| `MarinaName` | character varying | hayır |  |
| `Latitude` | double precision | evet |  |
| `Longitude` | double precision | evet |  |
| `CommercialCapacity` | integer | hayır |  |
| `LegalCapacity` | integer | hayır |  |
| `CabinCount` | integer | hayır |  |
| `BedCount` | integer | hayır |  |
| `BathroomCount` | integer | hayır |  |
| `LengthMeters` | numeric | evet |  |
| `WidthMeters` | numeric | evet |  |
| `BuildYear` | integer | evet |  |
| `LastRefitYear` | integer | evet |  |
| `EngineInfo` | character varying | evet |  |
| `FlagRegistryNo` | character varying | evet |  |
| `CaptainName` | character varying | evet |  |
| `CrewCount` | integer | hayır |  |
| `Status` | character varying | hayır |  |
| `DefaultCalendarMode` | character varying | hayır |  |
| `RequiresPassengerList` | boolean | hayır |  |
| `PassengerListReminderHours` | integer | hayır |  |
| `AverageRating` | numeric | evet |  |
| `ReviewCount` | integer | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `DraftMeters` | numeric | evet |  |

Kısıtlar:

- `CK_Boats_Capacity` — `CHECK ((("CommercialCapacity" > 0) AND ("CommercialCapacity" <= "LegalCapacity")))`
- `CK_Boats_DefaultCalendarMode_Enum` — `CHECK ((("DefaultCalendarMode")::text = ANY ((ARRAY['Shared'::character varying, 'ExclusiveOpen'::character varying])::text[])))`
- `CK_Boats_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Draft'::character varying, 'Published'::character varying, 'Inactive'::character varying])::text[])))`

## `CalendarModeRules`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `ValidFrom` | date | hayır |  |
| `ValidTo` | date | hayır |  |
| `Mode` | character varying | hayır |  |
| `Priority` | integer | hayır |  |
| `Note` | character varying | evet |  |
| `CreatedByUserId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_CalendarModeRules_Mode_Enum` — `CHECK ((("Mode")::text = ANY ((ARRAY['Shared'::character varying, 'ExclusiveOpen'::character varying])::text[])))`
- `CK_CalendarModeRules_Priority` — `CHECK (("Priority" >= 0))`
- `CK_CalendarModeRules_Range` — `CHECK (("ValidFrom" <= "ValidTo"))`
- `EX_CalendarModeRules_NoOverlapPerLayer` — `EXCLUDE USING gist ("BoatId" WITH =, "Priority" WITH =, daterange("ValidFrom", "ValidTo", '[]'::text) WITH &&)`

## `ConsentDocuments`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ConsentType` | character varying | hayır |  |
| `Version` | character varying | hayır |  |
| `BodyHtml` | text | hayır |  |
| `IsActive` | boolean | hayır |  |
| `EffectiveFrom` | timestamp with time zone | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_ConsentDocuments_ConsentType_Enum` — `CHECK ((("ConsentType")::text = ANY ((ARRAY['Cookies'::character varying, 'PrivacyPolicy'::character varying, 'TermsOfUse'::character varying, 'MarketingCommunication'::character varying])::text[])))`

## `ConsentRecords`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | hayır |  |
| `ConsentType` | character varying | hayır |  |
| `DocumentVersion` | character varying | hayır |  |
| `AcceptedAt` | timestamp with time zone | hayır |  |
| `Ip` | character varying | evet |  |
| `UserAgent` | character varying | evet |  |

Kısıtlar:

- `CK_ConsentRecords_ConsentType_Enum` — `CHECK ((("ConsentType")::text = ANY ((ARRAY['Cookies'::character varying, 'PrivacyPolicy'::character varying, 'TermsOfUse'::character varying, 'MarketingCommunication'::character varying])::text[])))`

## `ContractTemplates`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Name` | character varying | hayır |  |
| `BodyHtml` | text | hayır |  |
| `Version` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |
| `CreatedByUserId` | uuid | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `Contracts`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `TemplateId` | uuid | hayır |  |
| `TemplateVersion` | integer | hayır |  |
| `BodyHtmlSnapshot` | text | hayır |  |
| `CommissionRate` | numeric | hayır |  |
| `PayoutPeriodDays` | integer | hayır |  |
| `Status` | character varying | hayır |  |
| `SentAt` | timestamp with time zone | evet |  |
| `SentByUserId` | uuid | evet |  |
| `ApprovedAt` | timestamp with time zone | evet |  |
| `ApprovedByUserId` | uuid | evet |  |
| `ApprovedIp` | character varying | evet |  |
| `ApprovedUserAgent` | character varying | evet |  |
| `ValidFrom` | timestamp with time zone | evet |  |
| `ValidTo` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `RejectedAt` | timestamp with time zone | evet |  |
| `RejectedByUserId` | uuid | evet |  |
| `RejectionReason` | character varying | evet |  |

Kısıtlar:

- `CK_Contracts_ApprovedEvidence` — `CHECK (((("Status")::text <> 'Approved'::text) OR (("ApprovedAt" IS NOT NULL) AND ("ApprovedByUserId" IS NOT NULL))))`
- `CK_Contracts_CommissionRate` — `CHECK ((("CommissionRate" >= (0)::numeric) AND ("CommissionRate" <= (100)::numeric)))`
- `CK_Contracts_PayoutPeriodDays` — `CHECK (("PayoutPeriodDays" > 0))`
- `CK_Contracts_RejectedEvidence` — `CHECK (((("Status")::text <> 'Rejected'::text) OR (("RejectedAt" IS NOT NULL) AND ("RejectedByUserId" IS NOT NULL) AND ("RejectionReason" IS NOT NULL))))`
- `CK_Contracts_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Draft'::character varying, 'Sent'::character varying, 'Approved'::character varying, 'Cancelled'::character varying, 'Rejected'::character varying])::text[])))`

## `ConversationReservations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `ConversationId` | uuid | hayır |  |
| `ReservationId` | uuid | hayır |  |
| `LinkedAt` | timestamp with time zone | hayır |  |

## `Conversations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `CustomerUserId` | uuid | hayır |  |
| `Status` | character varying | hayır |  |
| `CloseReason` | character varying | evet |  |
| `ClosedAt` | timestamp with time zone | evet |  |
| `LastMessageAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Conversations_CloseReason_Enum` — `CHECK ((("CloseReason" IS NULL) OR (("CloseReason")::text = ANY ((ARRAY['Boarded'::character varying, 'DatePassed'::character varying, 'Manual'::character varying])::text[]))))`
- `CK_Conversations_Closed` — `CHECK (((("Status")::text <> 'Closed'::text) OR (("ClosedAt" IS NOT NULL) AND ("CloseReason" IS NOT NULL))))`
- `CK_Conversations_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Open'::character varying, 'Closed'::character varying])::text[])))`

## `CouponAssignments`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `CouponId` | uuid | hayır |  |
| `UserId` | uuid | hayır |  |
| `AssignedAt` | timestamp with time zone | hayır |  |

## `CouponRedemptions`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `CouponId` | uuid | hayır |  |
| `ReservationId` | uuid | hayır |  |
| `DiscountAmountTry` | numeric | hayır |  |
| `AppliedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_CouponRedemptions_Amount` — `CHECK (("DiscountAmountTry" >= (0)::numeric))`

## `Coupons`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Code` | USER-DEFINED | hayır |  |
| `Percentage` | numeric | hayır |  |
| `ValidFrom` | timestamp with time zone | hayır |  |
| `ValidTo` | timestamp with time zone | hayır |  |
| `MaxRedemptions` | integer | evet |  |
| `UsedCount` | integer | hayır |  |
| `PartnerId` | uuid | evet |  |
| `BoatId` | uuid | evet |  |
| `IsActive` | boolean | hayır |  |
| `CreatedByUserId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `FundedBy` | text | hayır |  |
| `IsPubliclyListed` | boolean | hayır |  |
| `Title` | character varying | evet |  |

Kısıtlar:

- `CK_Coupons_FundedBy` — `CHECK ((("FundedBy" <> 'Partner'::text) OR ("PartnerId" IS NOT NULL)))`
- `CK_Coupons_FundedByValue` — `CHECK (("FundedBy" = ANY (ARRAY['Platform'::text, 'Partner'::text])))`
- `CK_Coupons_FundedBy_Enum` — `CHECK (("FundedBy" = ANY (ARRAY['Platform'::text, 'Partner'::text])))`
- `CK_Coupons_Percentage` — `CHECK ((("Percentage" > (0)::numeric) AND ("Percentage" <= (100)::numeric)))`
- `CK_Coupons_Redemptions` — `CHECK ((("UsedCount" >= 0) AND (("MaxRedemptions" IS NULL) OR ("UsedCount" <= "MaxRedemptions"))))`
- `CK_Coupons_Validity` — `CHECK (("ValidFrom" < "ValidTo"))`

## `EventLogs`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Seq` | bigint | hayır |  |
| `OccurredAt` | timestamp with time zone | hayır |  |
| `EventType` | character varying | hayır |  |
| `ActorType` | character varying | hayır |  |
| `ActorUserId` | uuid | evet |  |
| `SessionId` | character varying | evet |  |
| `SubjectType` | character varying | evet |  |
| `SubjectId` | uuid | evet |  |
| `PartnerId` | uuid | evet |  |
| `BoatId` | uuid | evet |  |
| `Payload` | jsonb | evet |  |
| `IpHash` | character varying | evet |  |
| `UserAgent` | character varying | evet |  |

Kısıtlar:

- `CK_EventLogs_ActorType_Enum` — `CHECK ((("ActorType")::text = ANY ((ARRAY['Customer'::character varying, 'BoatOwner'::character varying, 'Platform'::character varying, 'System'::character varying, 'Anonymous'::character varying])::text[])))`

## `ExchangeRates`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Date` | date | hayır |  |
| `CurrencyCode` | character varying | hayır |  |
| `RateToTry` | numeric | hayır |  |
| `Source` | character varying | hayır |  |
| `FetchedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_ExchangeRates_CurrencyCode_Enum` — `CHECK ((("CurrencyCode")::text = ANY ((ARRAY['TRY'::character varying, 'USD'::character varying, 'EUR'::character varying, 'GBP'::character varying])::text[])))`
- `CK_ExchangeRates_Positive` — `CHECK (("RateToTry" > (0)::numeric))`

## `ExtraTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ExtraId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Description` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_ExtraTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `Extras`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatRentalTypeId` | uuid | hayır |  |
| `ExtraType` | character varying | hayır |  |
| `Price` | numeric | hayır |  |
| `IsActive` | boolean | hayır |  |
| `SortOrder` | integer | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Extras_ExtraType_Enum` — `CHECK ((("ExtraType")::text = ANY ((ARRAY['Menu'::character varying, 'Service'::character varying])::text[])))`
- `CK_Extras_Price` — `CHECK (("Price" >= (0)::numeric))`

## `FavoriteBoats`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | hayır |  |
| `BoatId` | uuid | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `InvoiceCounters`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Series` | character varying | hayır |  |
| `LastNumber` | bigint | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_InvoiceCounters_LastNumber` — `CHECK (("LastNumber" >= 0))`

## `Invoices`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `IssuerType` | character varying | hayır |  |
| `IssuerPartnerId` | uuid | evet |  |
| `RecipientType` | character varying | hayır |  |
| `RecipientPartnerId` | uuid | evet |  |
| `RecipientName` | character varying | evet |  |
| `InvoiceType` | character varying | hayır |  |
| `Number` | character varying | hayır |  |
| `IssuedAt` | timestamp with time zone | hayır |  |
| `AmountTry` | numeric | hayır |  |
| `TaxAmountTry` | numeric | hayır |  |
| `PayoutId` | uuid | evet |  |
| `FileKey` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Invoices_InvoiceType_Enum` — `CHECK ((("InvoiceType")::text = ANY ((ARRAY['Commission'::character varying, 'Service'::character varying])::text[])))`
- `CK_Invoices_IssuerType_Enum` — `CHECK ((("IssuerType")::text = ANY ((ARRAY['Platform'::character varying, 'Partner'::character varying, 'Customer'::character varying])::text[])))`
- `CK_Invoices_RecipientType_Enum` — `CHECK ((("RecipientType")::text = ANY ((ARRAY['Platform'::character varying, 'Partner'::character varying, 'Customer'::character varying])::text[])))`

## `JobRuns`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `JobName` | character varying | hayır |  |
| `StartedAt` | timestamp with time zone | hayır |  |
| `CompletedAt` | timestamp with time zone | evet |  |
| `Succeeded` | boolean | hayır |  |
| `ItemsProcessed` | integer | hayır |  |
| `Error` | character varying | evet |  |

## `LedgerEntries`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | evet |  |
| `PartnerId` | uuid | evet |  |
| `AccountType` | character varying | hayır |  |
| `EntryType` | character varying | hayır |  |
| `Amount` | numeric | hayır |  |
| `ReversesEntryId` | uuid | evet |  |
| `PayoutId` | uuid | evet |  |
| `Note` | character varying | evet |  |
| `OccurredAt` | timestamp with time zone | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `RefundId` | uuid | evet |  |
| `PaymentId` | uuid | evet |  |

Kısıtlar:

- `CK_LedgerEntries_AccountType_Enum` — `CHECK ((("AccountType")::text = ANY ((ARRAY['Customer'::character varying, 'Platform'::character varying, 'Partner'::character varying])::text[])))`
- `CK_LedgerEntries_EntryType_Enum` — `CHECK ((("EntryType")::text = ANY ((ARRAY['Collection'::character varying, 'Commission'::character varying, 'PartnerEarning'::character varying, 'Refund'::character varying, 'CouponCost'::character varying, 'Correction'::character varying])::text[])))`
- `CK_LedgerEntries_Odeme_Bagi` — `CHECK (((("EntryType")::text = ANY ((ARRAY['Collection'::character varying, 'PartnerEarning'::character varying])::text[])) = ("PaymentId" IS NOT NULL)))`
- `CK_LedgerEntries_Refund_Bagi` — `CHECK (((("EntryType")::text = 'Refund'::text) = ("RefundId" IS NOT NULL)))`

## `Messages`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ConversationId` | uuid | hayır |  |
| `SenderUserId` | uuid | hayır |  |
| `SenderRole` | character varying | hayır |  |
| `Body` | text | hayır |  |
| `MaskedBody` | text | hayır |  |
| `MaskedItemCount` | integer | hayır |  |
| `ReadAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Messages_MaskedItemCount` — `CHECK (("MaskedItemCount" >= 0))`
- `CK_Messages_SenderRole_Enum` — `CHECK ((("SenderRole")::text = ANY ((ARRAY['Customer'::character varying, 'BoatOwner'::character varying])::text[])))`

## `NotificationDeliveries`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `NotificationId` | uuid | hayır |  |
| `Channel` | character varying | hayır |  |
| `Provider` | character varying | evet |  |
| `ProviderMessageId` | character varying | evet |  |
| `Status` | character varying | hayır |  |
| `SentAt` | timestamp with time zone | evet |  |
| `FailedAt` | timestamp with time zone | evet |  |
| `Error` | character varying | evet |  |
| `AttemptCount` | integer | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_NotificationDeliveries_AttemptCount` — `CHECK (("AttemptCount" >= 0))`
- `CK_NotificationDeliveries_Channel_Enum` — `CHECK ((("Channel")::text = ANY ((ARRAY['Email'::character varying, 'Sms'::character varying, 'InApp'::character varying])::text[])))`
- `CK_NotificationDeliveries_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Queued'::character varying, 'Sent'::character varying, 'Failed'::character varying, 'Bounced'::character varying])::text[])))`

## `NotificationOutbox`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Channel` | character varying | hayır |  |
| `Recipient` | character varying | hayır |  |
| `Subject` | character varying | evet |  |
| `Body` | character varying | hayır |  |
| `Reference` | character varying | evet |  |
| `Status` | character varying | hayır |  |
| `Attempts` | integer | hayır |  |
| `NextAttemptAt` | timestamp with time zone | hayır |  |
| `LastError` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `NotificationId` | uuid | evet |  |
| `TemplateKey` | text | hayır | `''::text` |

Kısıtlar:

- `CK_NotificationOutbox_Attempts` — `CHECK (("Attempts" >= 0))`
- `CK_NotificationOutbox_Channel_Enum` — `CHECK ((("Channel")::text = ANY ((ARRAY['Email'::character varying, 'Sms'::character varying, 'InApp'::character varying])::text[])))`
- `CK_NotificationOutbox_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Pending'::character varying, 'Failed'::character varying])::text[])))`

## `NotificationPreferences`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | hayır |  |
| `EmailEnabled` | boolean | hayır |  |
| `SmsEnabled` | boolean | hayır |  |
| `ReviewInvitationsEnabled` | boolean | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_NotificationPreferences_AtLeastOneChannel` — `CHECK (("EmailEnabled" OR "SmsEnabled"))`

## `NotificationTemplates`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Channel` | character varying | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Subject` | character varying | evet |  |
| `Body` | text | hayır |  |
| `IsActive` | boolean | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_NotificationTemplates_Channel_Enum` — `CHECK ((("Channel")::text = ANY ((ARRAY['Email'::character varying, 'Sms'::character varying, 'InApp'::character varying])::text[])))`

## `Notifications`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | evet |  |
| `RecipientEmail` | USER-DEFINED | evet |  |
| `RecipientPhone` | character varying | evet |  |
| `TemplateKey` | character varying | hayır |  |
| `Payload` | jsonb | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Notifications_Recipient` — `CHECK ((("UserId" IS NOT NULL) OR ("RecipientEmail" IS NOT NULL) OR ("RecipientPhone" IS NOT NULL)))`

## `OfferItems`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `OfferId` | uuid | hayır |  |
| `ExtraId` | uuid | hayır |  |
| `NameSnapshot` | character varying | hayır |  |
| `UnitPrice` | numeric | hayır |  |
| `Quantity` | integer | hayır |  |

Kısıtlar:

- `CK_OfferItems_Quantity` — `CHECK (("Quantity" > 0))`

## `Offers`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ConversationId` | uuid | hayır |  |
| `BoatRentalTypeId` | uuid | hayır |  |
| `VoyageId` | uuid | hayır |  |
| `CreatedByUserId` | uuid | hayır |  |
| `CustomerUserId` | uuid | hayır |  |
| `AdultCount` | integer | hayır |  |
| `ChildCount` | integer | hayır |  |
| `InfantCount` | integer | hayır |  |
| `TotalAmount` | numeric | hayır |  |
| `Currency` | character varying | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `Status` | character varying | hayır |  |
| `Note` | character varying | evet |  |
| `ReservationId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `RespondedAt` | timestamp with time zone | evet |  |

Kısıtlar:

- `CK_Offers_Accepted` — `CHECK (((("Status")::text <> 'Accepted'::text) OR ("ReservationId" IS NOT NULL)))`
- `CK_Offers_Amount` — `CHECK (("TotalAmount" > (0)::numeric))`
- `CK_Offers_Counts` — `CHECK ((("AdultCount" >= 0) AND ("ChildCount" >= 0) AND ("InfantCount" >= 0)))`
- `CK_Offers_Currency_Enum` — `CHECK ((("Currency")::text = ANY ((ARRAY['TRY'::character varying, 'USD'::character varying, 'EUR'::character varying, 'GBP'::character varying])::text[])))`
- `CK_Offers_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Sent'::character varying, 'Accepted'::character varying, 'Rejected'::character varying, 'Expired'::character varying, 'Cancelled'::character varying])::text[])))`

## `PartnerDocuments`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `DocumentType` | character varying | hayır |  |
| `FileKey` | character varying | hayır |  |
| `UploadedAt` | timestamp with time zone | hayır |  |
| `RejectionReason` | character varying | evet |  |
| `ReviewNote` | character varying | evet |  |
| `ReviewedAt` | timestamp with time zone | evet |  |
| `ReviewedByUserId` | uuid | evet |  |
| `Status` | character varying | hayır | `''::character varying` |

Kısıtlar:

- `CK_PartnerDocuments_DocumentType_Enum` — `CHECK ((("DocumentType")::text = ANY ((ARRAY['TaxCertificate'::character varying, 'IdentityDocument'::character varying, 'TradeRegistry'::character varying, 'Other'::character varying])::text[])))`
- `CK_PartnerDocuments_RedSebebi` — `CHECK ((("RejectionReason" IS NULL) OR (("Status")::text = 'Rejected'::text)))`
- `CK_PartnerDocuments_RejectionReason_Enum` — `CHECK ((("RejectionReason" IS NULL) OR (("RejectionReason")::text = ANY ((ARRAY['Unreadable'::character varying, 'Expired'::character varying, 'WrongDocument'::character varying, 'MismatchedInfo'::character varying])::text[]))))`
- `CK_PartnerDocuments_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Pending'::character varying, 'Verified'::character varying, 'Rejected'::character varying, 'Expired'::character varying])::text[])))`

## `PartnerMembers`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `UserId` | uuid | hayır |  |
| `RoleId` | uuid | hayır |  |
| `IsOwner` | boolean | hayır |  |
| `Status` | character varying | hayır |  |
| `InvitedByUserId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_PartnerMembers_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Active'::character varying, 'Inactive'::character varying])::text[])))`

## `PartnerPayeeAccounts`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `Provider` | character varying | hayır |  |
| `ExternalKey` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `RawResponse` | jsonb | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_PartnerPayeeAccounts_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Registered'::character varying, 'Blocked'::character varying])::text[])))`

## `Partners`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `LegalName` | character varying | hayır |  |
| `DisplayName` | character varying | hayır |  |
| `TaxNumber` | character varying | hayır |  |
| `TaxOffice` | character varying | evet |  |
| `Email` | USER-DEFINED | hayır |  |
| `Phone` | character varying | hayır |  |
| `Address` | text | evet |  |
| `City` | character varying | evet |  |
| `Status` | character varying | hayır |  |
| `RejectionReason` | text | evet |  |
| `AppliedAt` | timestamp with time zone | hayır |  |
| `ApprovedAt` | timestamp with time zone | evet |  |
| `RejectedAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `SuspensionReason` | text | evet |  |
| `BusinessType` | character varying | evet |  |
| `Iban` | character varying | evet |  |
| `District` | character varying | evet |  |
| `TursabNumber` | character varying | evet |  |
| `TursabVerifiedAt` | timestamp with time zone | evet |  |

Kısıtlar:

- `CK_Partners_BusinessType_Enum` — `CHECK ((("BusinessType" IS NULL) OR (("BusinessType")::text = ANY ((ARRAY['Personal'::character varying, 'PrivateCompany'::character varying, 'LimitedOrJointStock'::character varying])::text[]))))`
- `CK_Partners_Iban` — `CHECK ((("Iban" IS NULL) OR (("Iban")::text ~ '^TR[0-9]{24}$'::text)))`
- `CK_Partners_RejectionReason` — `CHECK (((("Status")::text <> 'Rejected'::text) OR ("RejectionReason" IS NOT NULL)))`
- `CK_Partners_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['ApplicationReceived'::character varying, 'UnderReview'::character varying, 'ContractSent'::character varying, 'Active'::character varying, 'Rejected'::character varying, 'Suspended'::character varying])::text[])))`
- `CK_Partners_TursabVerified` — `CHECK ((("TursabVerifiedAt" IS NULL) OR ("TursabNumber" IS NOT NULL)))`

## `Passengers`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `FullName` | character varying | hayır |  |
| `BirthDate` | date | hayır |  |
| `IdentityType` | character varying | hayır |  |
| `IdentityNumber` | character varying | hayır |  |
| `Nationality` | character varying | evet |  |
| `FilledByUserId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Passengers_IdentityType_Enum` — `CHECK ((("IdentityType")::text = ANY ((ARRAY['Tckn'::character varying, 'Passport'::character varying, 'ForeignerId'::character varying])::text[])))`

## `Payments`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `Provider` | character varying | hayır |  |
| `ProviderTransactionId` | character varying | evet |  |
| `AmountTry` | numeric | hayır |  |
| `Status` | character varying | hayır |  |
| `RawResponse` | jsonb | evet |  |
| `IdempotencyKey` | character varying | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `CompletedAt` | timestamp with time zone | evet |  |
| `CollectedByStaffId` | uuid | evet |  |
| `ManualMethod` | character varying | evet |  |
| `Note` | character varying | evet |  |

Kısıtlar:

- `CK_Payments_Amount` — `CHECK (("AmountTry" > (0)::numeric))`
- `CK_Payments_ElleTahsilat` — `CHECK (((("ManualMethod" IS NULL) AND ("CollectedByStaffId" IS NULL)) OR ((("Provider")::text = 'manual'::text) AND ("ManualMethod" IS NOT NULL))))`
- `CK_Payments_ManualMethod_Enum` — `CHECK ((("ManualMethod" IS NULL) OR (("ManualMethod")::text = ANY ((ARRAY['Cash'::character varying, 'BankTransfer'::character varying, 'PosAtOffice'::character varying, 'Other'::character varying])::text[]))))`
- `CK_Payments_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Initiated'::character varying, 'Succeeded'::character varying, 'Failed'::character varying, 'Refunded'::character varying])::text[])))`

## `Payouts`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `PartnerId` | uuid | hayır |  |
| `PeriodStart` | date | hayır |  |
| `PeriodEnd` | date | hayır |  |
| `TotalAmountTry` | numeric | hayır |  |
| `Status` | character varying | hayır |  |
| `ProviderInstructionId` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `SettledAt` | timestamp with time zone | evet |  |

Kısıtlar:

- `CK_Payouts_Amount` — `CHECK (("TotalAmountTry" >= (0)::numeric))`
- `CK_Payouts_Period` — `CHECK (("PeriodStart" <= "PeriodEnd"))`
- `CK_Payouts_Settled` — `CHECK (((("Status")::text <> 'Settled'::text) OR ("SettledAt" IS NOT NULL)))`
- `CK_Payouts_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Prepared'::character varying, 'InstructionSent'::character varying, 'Settled'::character varying, 'Failed'::character varying])::text[])))`

## `Permissions`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Category` | character varying | hayır |  |
| `IsPartnerAssignable` | boolean | hayır |  |

## `PlatformSettings`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | integer | hayır |  |
| `HoldMinutes` | integer | hayır |  |
| `CollectionWindowHours` | integer | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `UpdatedByUserId` | uuid | evet |  |

Kısıtlar:

- `CK_PlatformSettings_TahsilatPenceresi` — `CHECK ((("CollectionWindowHours" >= 1) AND ("CollectionWindowHours" <= 168)))`
- `CK_PlatformSettings_TekSatir` — `CHECK (("Id" = 1))`
- `CK_PlatformSettings_TutmaSuresi` — `CHECK ((("HoldMinutes" >= 1) AND ("HoldMinutes" <= 120)))`

## `Prices`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatRentalTypeId` | uuid | hayır |  |
| `ValidFrom` | date | evet |  |
| `ValidTo` | date | evet |  |
| `AdultPrice` | numeric | evet |  |
| `ChildPrice` | numeric | evet |  |
| `InfantPrice` | numeric | evet |  |
| `BoatPrice` | numeric | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Prices_HasAnyPrice` — `CHECK ((("AdultPrice" IS NOT NULL) OR ("BoatPrice" IS NOT NULL)))`
- `CK_Prices_NonNegative` — `CHECK (((COALESCE("AdultPrice", (0)::numeric) >= (0)::numeric) AND (COALESCE("ChildPrice", (0)::numeric) >= (0)::numeric) AND (COALESCE("InfantPrice", (0)::numeric) >= (0)::numeric) AND (COALESCE("BoatPrice", (0)::numeric) >= (0)::numeric)))`
- `CK_Prices_RangeComplete` — `CHECK (((("ValidFrom" IS NULL) AND ("ValidTo" IS NULL)) OR (("ValidFrom" IS NOT NULL) AND ("ValidTo" IS NOT NULL) AND ("ValidFrom" <= "ValidTo"))))`
- `EX_Prices_NoOverlappingSeasons` — `EXCLUDE USING gist ("BoatRentalTypeId" WITH =, daterange("ValidFrom", "ValidTo", '[]'::text) WITH &&) WHERE (("ValidFrom" IS NOT NULL))`

## `RefreshTokens`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | hayır |  |
| `TokenSha256` | character varying | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `RevokedAt` | timestamp with time zone | evet |  |
| `ReplacedById` | uuid | evet |  |
| `CreatedIp` | character varying | evet |  |
| `UserAgent` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `Refunds`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `PaymentId` | uuid | evet |  |
| `AmountTry` | numeric | hayır |  |
| `Reason` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `RequestedByUserId` | uuid | evet |  |
| `ProviderRefundId` | character varying | evet |  |
| `RawResponse` | jsonb | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `CompletedAt` | timestamp with time zone | evet |  |
| `IdempotencyKey` | character varying | hayır | `''::character varying` |
| `Attempts` | integer | hayır | `0` |
| `LastAttemptAt` | timestamp with time zone | evet |  |

Kısıtlar:

- `CK_Refunds_Amount` — `CHECK (("AmountTry" > (0)::numeric))`
- `CK_Refunds_Reason_Enum` — `CHECK ((("Reason")::text = ANY ((ARRAY['CustomerCancellation'::character varying, 'WeatherCancellation'::character varying, 'NoShow'::character varying, 'PartnerCancellation'::character varying, 'PlatformDecision'::character varying])::text[])))`
- `CK_Refunds_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Requested'::character varying, 'Sent'::character varying, 'Completed'::character varying, 'Failed'::character varying])::text[])))`

## `RegionTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `RegionId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Description` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_RegionTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `Regions`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Slug` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |

## `RentalTypeTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `RentalTypeId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Description` | text | evet |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_RentalTypeTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `RentalTypes`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `PricingStrategy` | character varying | hayır |  |
| `OccupancyMode` | character varying | hayır |  |
| `DurationKind` | character varying | hayır |  |
| `ExtraDayCount` | integer | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |
| `SupportsDivers` | boolean | hayır | `false` |

Kısıtlar:

- `CK_RentalTypes_DurationKind_Enum` — `CHECK ((("DurationKind")::text = ANY ((ARRAY['WithinDay'::character varying, 'MultiDay'::character varying])::text[])))`
- `CK_RentalTypes_ExtraDayCount` — `CHECK (("ExtraDayCount" >= 0))`
- `CK_RentalTypes_OccupancyMode_Enum` — `CHECK ((("OccupancyMode")::text = ANY ((ARRAY['Shared'::character varying, 'Exclusive'::character varying])::text[])))`
- `CK_RentalTypes_PricingStrategy_Enum` — `CHECK ((("PricingStrategy")::text = ANY ((ARRAY['PerPerson'::character varying, 'PerBoat'::character varying])::text[])))`

## `RequestLogs`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `OccurredAt` | timestamp with time zone | hayır |  |
| `Method` | character varying | hayır |  |
| `Path` | character varying | hayır |  |
| `RouteTemplate` | character varying | evet |  |
| `Query` | character varying | evet |  |
| `StatusCode` | integer | hayır |  |
| `DurationMs` | integer | hayır |  |
| `ActorUserId` | uuid | evet |  |
| `ActorType` | character varying | hayır |  |
| `IpHash` | character varying | evet |  |
| `UserAgent` | character varying | evet |  |
| `TraceId` | character varying | evet |  |

Kısıtlar:

- `CK_RequestLogs_ActorType_Enum` — `CHECK ((("ActorType")::text = ANY ((ARRAY['Customer'::character varying, 'BoatOwner'::character varying, 'Platform'::character varying, 'System'::character varying, 'Anonymous'::character varying])::text[])))`

## `RescheduleRequests`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `TargetDate` | date | hayır |  |
| `NewTotalTry` | numeric | hayır |  |
| `DifferenceTry` | numeric | hayır |  |
| `Status` | character varying | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `PaymentId` | uuid | evet |  |
| `CreatedByUserId` | uuid | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `ResolvedAt` | timestamp with time zone | evet |  |
| `TokenSha256` | character varying | hayır | `''::character varying` |

Kısıtlar:

- `CK_RescheduleRequests_Difference` — `CHECK (("DifferenceTry" > (0)::numeric))`
- `CK_RescheduleRequests_Status_Enum` — `CHECK ((("Status")::text = ANY (ARRAY[('AwaitingPayment'::character varying)::text, ('PaymentFailed'::character varying)::text, ('Completed'::character varying)::text, ('Expired'::character varying)::text, ('Cancelled'::character varying)::text, ('DroppedOnCancellation'::character varying)::text])))`

## `ReservationExtras`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `ExtraId` | uuid | hayır |  |
| `ExtraType` | character varying | hayır |  |
| `NameSnapshot` | character varying | hayır |  |
| `UnitPrice` | numeric | hayır |  |
| `Quantity` | integer | hayır |  |
| `LineTotalTry` | numeric | hayır |  |

Kısıtlar:

- `CK_ReservationExtras_ExtraType_Enum` — `CHECK ((("ExtraType")::text = ANY ((ARRAY['Menu'::character varying, 'Service'::character varying])::text[])))`
- `CK_ReservationExtras_Quantity` — `CHECK (("Quantity" > 0))`

## `ReservationStatusHistories`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `FromStatus` | character varying | hayır |  |
| `ToStatus` | character varying | hayır |  |
| `ChangedByUserId` | uuid | evet |  |
| `Reason` | character varying | evet |  |
| `ChangedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_ReservationStatusHistories_FromStatus_Enum` — `CHECK ((("FromStatus")::text = ANY ((ARRAY['Pending'::character varying, 'AwaitingCollection'::character varying, 'Paid'::character varying, 'Boarded'::character varying, 'Completed'::character varying, 'Expired'::character varying, 'Cancelled'::character varying, 'Refunded'::character varying])::text[])))`
- `CK_ReservationStatusHistories_ToStatus_Enum` — `CHECK ((("ToStatus")::text = ANY ((ARRAY['Pending'::character varying, 'AwaitingCollection'::character varying, 'Paid'::character varying, 'Boarded'::character varying, 'Completed'::character varying, 'Expired'::character varying, 'Cancelled'::character varying, 'Refunded'::character varying])::text[])))`

## `Reservations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Code` | character varying | hayır |  |
| `VoyageId` | uuid | hayır |  |
| `BoatRentalTypeId` | uuid | hayır |  |
| `UserId` | uuid | evet |  |
| `ContactFullName` | character varying | hayır |  |
| `ContactEmail` | USER-DEFINED | hayır |  |
| `ContactPhone` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `HoldExpiresAt` | timestamp with time zone | evet |  |
| `AdultCount` | integer | hayır |  |
| `ChildCount` | integer | hayır |  |
| `InfantCount` | integer | hayır |  |
| `AdultUnitPrice` | numeric | evet |  |
| `ChildUnitPrice` | numeric | evet |  |
| `InfantUnitPrice` | numeric | evet |  |
| `BoatPrice` | numeric | evet |  |
| `InfantMaxAge` | integer | hayır |  |
| `ChildMaxAge` | integer | hayır |  |
| `ListCurrency` | character varying | hayır |  |
| `ListTotal` | numeric | hayır |  |
| `ExchangeRate` | numeric | hayır |  |
| `ExchangeRateDate` | date | hayır |  |
| `TotalTry` | numeric | hayır |  |
| `CommissionRate` | numeric | hayır |  |
| `ContractId` | uuid | hayır |  |
| `RequiresPassengerList` | boolean | hayır |  |
| `ExtrasTotalTry` | numeric | hayır |  |
| `CouponId` | uuid | evet |  |
| `DiscountAmountTry` | numeric | hayır |  |
| `GrandTotalTry` | numeric | hayır |  |
| `BoardingTokenSha256` | character varying | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `PaidAt` | timestamp with time zone | evet |  |
| `BoardedAt` | timestamp with time zone | evet |  |
| `CompletedAt` | timestamp with time zone | evet |  |
| `CancelledAt` | timestamp with time zone | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `BoardingTokenExpiresAt` | timestamp with time zone | evet |  |
| `CouponFundedBy` | text | evet |  |
| `PlatformAbsorbedTry` | numeric | hayır | `0.0` |
| `IdempotencyKey` | character varying | hayır |  |
| `CancellationRefundRate` | numeric | evet |  |
| `RefundDueTry` | numeric | evet |  |
| `RefundReason` | character varying | evet |  |
| `VatRate` | numeric | hayır |  |
| `DiverCount` | integer | hayır | `0` |
| `CancellationNote` | character varying | evet |  |
| `CancellationReason` | character varying | evet |  |
| `CreatedByStaffId` | uuid | evet |  |
| `PaymentLinkSentAt` | timestamp with time zone | evet |  |
| `PaymentLinkSentCount` | integer | hayır | `0` |
| `PaymentLinkTokenEncrypted` | text | evet |  |
| `PaymentLinkTokenSha256` | character varying | evet |  |

Kısıtlar:

- `CK_Reservations_AgeLimits` — `CHECK ((("InfantMaxAge" >= 0) AND ("ChildMaxAge" > "InfantMaxAge")))`
- `CK_Reservations_CancellationOtherNote` — `CHECK (((("CancellationReason")::text IS DISTINCT FROM 'Other'::text) OR (("CancellationNote" IS NOT NULL) AND (length(btrim(("CancellationNote")::text)) > 0))))`
- `CK_Reservations_CancellationReason_Enum` — `CHECK ((("CancellationReason" IS NULL) OR (("CancellationReason")::text = ANY ((ARRAY['PlansChanged'::character varying, 'Weather'::character varying, 'Health'::character varying, 'WrongBooking'::character varying, 'FoundAlternative'::character varying, 'Other'::character varying])::text[]))))`
- `CK_Reservations_CommissionRate` — `CHECK ((("CommissionRate" >= (0)::numeric) AND ("CommissionRate" <= (100)::numeric)))`
- `CK_Reservations_Counts` — `CHECK ((("AdultCount" >= 0) AND ("ChildCount" >= 0) AND ("InfantCount" >= 0) AND ((("AdultCount" + "ChildCount") + "InfantCount") > 0)))`
- `CK_Reservations_CouponFundedBy` — `CHECK ((("CouponId" IS NULL) = ("CouponFundedBy" IS NULL)))`
- `CK_Reservations_CouponFundedByValue` — `CHECK ((("CouponFundedBy" IS NULL) OR ("CouponFundedBy" = ANY (ARRAY['Platform'::text, 'Partner'::text]))))`
- `CK_Reservations_CouponFundedBy_Enum` — `CHECK ((("CouponFundedBy" IS NULL) OR ("CouponFundedBy" = ANY (ARRAY['Platform'::text, 'Partner'::text]))))`
- `CK_Reservations_DiscountBound` — `CHECK (("DiscountAmountTry" <= ("TotalTry" + "ExtrasTotalTry")))`
- `CK_Reservations_DiverCount` — `CHECK ((("DiverCount" >= 0) AND ("DiverCount" <= ("AdultCount" + "ChildCount"))))`
- `CK_Reservations_ExchangeRate` — `CHECK (("ExchangeRate" > (0)::numeric))`
- `CK_Reservations_GrandTotal` — `CHECK (("GrandTotalTry" = (("TotalTry" + "ExtrasTotalTry") - "DiscountAmountTry")))`
- `CK_Reservations_HoldExpiry` — `CHECK (((("Status")::text <> ALL ((ARRAY['Pending'::character varying, 'AwaitingCollection'::character varying])::text[])) OR ("HoldExpiresAt" IS NOT NULL)))`
- `CK_Reservations_ListCurrency_Enum` — `CHECK ((("ListCurrency")::text = ANY ((ARRAY['TRY'::character varying, 'USD'::character varying, 'EUR'::character varying, 'GBP'::character varying])::text[])))`
- `CK_Reservations_PaidAt` — `CHECK (((("Status")::text <> ALL (ARRAY[('Paid'::character varying)::text, ('Boarded'::character varying)::text, ('Completed'::character varying)::text])) OR ("PaidAt" IS NOT NULL)))`
- `CK_Reservations_PlatformAbsorbed` — `CHECK ((("PlatformAbsorbedTry" >= (0)::numeric) AND ("PlatformAbsorbedTry" <= "DiscountAmountTry")))`
- `CK_Reservations_RefundDue` — `CHECK (((("CancellationRefundRate" IS NULL) = ("RefundDueTry" IS NULL)) AND (("RefundDueTry" IS NULL) OR (("RefundDueTry" >= (0)::numeric) AND ("RefundDueTry" <= "GrandTotalTry")))))`
- `CK_Reservations_RefundRate` — `CHECK ((("CancellationRefundRate" IS NULL) OR ("CancellationRefundRate" = ANY (ARRAY[(0)::numeric, (50)::numeric, (100)::numeric]))))`
- `CK_Reservations_RefundReason_Enum` — `CHECK ((("RefundReason" IS NULL) OR (("RefundReason")::text = ANY ((ARRAY['CustomerCancellation'::character varying, 'WeatherCancellation'::character varying, 'NoShow'::character varying, 'PartnerCancellation'::character varying, 'PlatformDecision'::character varying])::text[]))))`
- `CK_Reservations_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Pending'::character varying, 'AwaitingCollection'::character varying, 'Paid'::character varying, 'Boarded'::character varying, 'Completed'::character varying, 'Expired'::character varying, 'Cancelled'::character varying, 'Refunded'::character varying])::text[])))`
- `CK_Reservations_TotalTry` — `CHECK ((abs(("TotalTry" - round(("ListTotal" * "ExchangeRate"), 2))) <= 0.01))`
- `CK_Reservations_Totals` — `CHECK ((("GrandTotalTry" >= (0)::numeric) AND ("DiscountAmountTry" >= (0)::numeric) AND ("ExtrasTotalTry" >= (0)::numeric)))`
- `CK_Reservations_VatRate` — `CHECK ((("VatRate" >= (0)::numeric) AND ("VatRate" <= (100)::numeric)))`

## `ReviewCriteria`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |

## `ReviewCriterionTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReviewCriterionId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_ReviewCriterionTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `ReviewInvitations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `TokenSha256` | character varying | hayır |  |
| `SentAt` | timestamp with time zone | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `UsedAt` | timestamp with time zone | evet |  |
| `ReminderSentAt` | timestamp with time zone | evet |  |

## `ReviewReplies`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReviewId` | uuid | hayır |  |
| `UserId` | uuid | hayır |  |
| `Body` | character varying | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `ReviewScores`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `ReviewId` | uuid | hayır |  |
| `ReviewCriterionId` | uuid | hayır |  |
| `Score` | smallint | hayır |  |

Kısıtlar:

- `CK_ReviewScores_Score` — `CHECK ((("Score" >= 1) AND ("Score" <= 5)))`

## `Reviews`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `ReservationId` | uuid | hayır |  |
| `BoatId` | uuid | hayır |  |
| `Rating` | smallint | hayır |  |
| `Body` | text | evet |  |
| `Status` | character varying | hayır |  |
| `ModeratedByUserId` | uuid | evet |  |
| `ModeratedAt` | timestamp with time zone | evet |  |
| `ModerationNote` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_Reviews_Moderated` — `CHECK (((("Status")::text = 'Pending'::text) OR (("ModeratedAt" IS NOT NULL) AND ("ModeratedByUserId" IS NOT NULL))))`
- `CK_Reviews_Rating` — `CHECK ((("Rating" >= 1) AND ("Rating" <= 5)))`
- `CK_Reviews_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Pending'::character varying, 'Approved'::character varying, 'Rejected'::character varying])::text[])))`

## `RolePermissions`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `RoleId` | uuid | hayır |  |
| `PermissionId` | uuid | hayır |  |

## `Roles`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `Name` | USER-DEFINED | hayır |  |
| `PartnerId` | uuid | evet |  |
| `IsSystem` | boolean | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `RuleTranslations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `RuleId` | uuid | hayır |  |
| `LanguageCode` | character varying | hayır |  |
| `Name` | character varying | hayır |  |
| `Source` | character varying | hayır |  |
| `SourceHash` | character varying | evet |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_RuleTranslations_Source_Enum` — `CHECK ((("Source")::text = ANY ((ARRAY['Manual'::character varying, 'Automatic'::character varying])::text[])))`

## `Rules`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Key` | character varying | hayır |  |
| `SortOrder` | integer | hayır |  |
| `IsActive` | boolean | hayır |  |

## `SupportMessages`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `SupportTicketId` | uuid | hayır |  |
| `SenderUserId` | uuid | evet |  |
| `Body` | text | hayır |  |
| `IsInternal` | boolean | hayır |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

## `SupportTickets`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Code` | character varying | hayır |  |
| `UserId` | uuid | evet |  |
| `ContactEmail` | USER-DEFINED | hayır |  |
| `ContactPhone` | character varying | evet |  |
| `Subject` | character varying | hayır |  |
| `Category` | character varying | hayır |  |
| `Priority` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `AssignedToUserId` | uuid | evet |  |
| `ReservationId` | uuid | evet |  |
| `FirstResponseAt` | timestamp with time zone | evet |  |
| `ResolvedAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_SupportTickets_Priority_Enum` — `CHECK ((("Priority")::text = ANY ((ARRAY['Low'::character varying, 'Normal'::character varying, 'High'::character varying, 'Urgent'::character varying])::text[])))`
- `CK_SupportTickets_Resolved` — `CHECK (((("Status")::text <> ALL ((ARRAY['Resolved'::character varying, 'Closed'::character varying])::text[])) OR ("ResolvedAt" IS NOT NULL)))`
- `CK_SupportTickets_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Open'::character varying, 'Answered'::character varying, 'Resolved'::character varying, 'Closed'::character varying])::text[])))`

## `TaxRates`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Rate` | numeric | hayır |  |
| `EffectiveFrom` | timestamp with time zone | hayır |  |
| `Note` | character varying | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_TaxRates_Rate` — `CHECK ((("Rate" >= (0)::numeric) AND ("Rate" <= (100)::numeric)))`

## `UserRoles`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `UserId` | uuid | hayır |  |
| `RoleId` | uuid | hayır |  |
| `GrantedByUserId` | uuid | evet |  |
| `GrantedAt` | timestamp with time zone | hayır |  |

## `UserTokens`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `UserId` | uuid | hayır |  |
| `Purpose` | character varying | hayır |  |
| `TokenSha256` | character varying | hayır |  |
| `ExpiresAt` | timestamp with time zone | hayır |  |
| `ConsumedAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `CreatedIp` | character varying | evet |  |
| `UserAgent` | character varying | evet |  |

Kısıtlar:

- `CK_UserTokens_Purpose_Enum` — `CHECK ((("Purpose")::text = ANY ((ARRAY['EmailVerification'::character varying, 'PasswordReset'::character varying, 'EmailChange'::character varying])::text[])))`

## `Users`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `Email` | USER-DEFINED | hayır |  |
| `EmailVerifiedAt` | timestamp with time zone | evet |  |
| `PendingEmail` | USER-DEFINED | evet |  |
| `PasswordHash` | text | hayır |  |
| `FullName` | character varying | hayır |  |
| `Phone` | character varying | hayır |  |
| `PhoneVerifiedAt` | timestamp with time zone | evet |  |
| `PreferredLanguage` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `LastLoginAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `AnonymizedAt` | timestamp with time zone | evet |  |
| `SecurityStamp` | uuid | hayır | `uuidv7()` |
| `MustChangePassword` | boolean | hayır | `false` |

Kısıtlar:

- `CK_Users_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Active'::character varying, 'Suspended'::character varying, 'Closed'::character varying])::text[])))`

## `VoyageStatusHistories`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `VoyageId` | uuid | hayır |  |
| `FromStatus` | character varying | hayır |  |
| `ToStatus` | character varying | hayır |  |
| `ChangedByUserId` | uuid | evet |  |
| `Reason` | character varying | evet |  |
| `ChangedAt` | timestamp with time zone | hayır |  |

Kısıtlar:

- `CK_VoyageStatusHistories_FromStatus_Enum` — `CHECK ((("FromStatus")::text = ANY ((ARRAY['Planned'::character varying, 'Completed'::character varying, 'Cancelled'::character varying])::text[])))`
- `CK_VoyageStatusHistories_ToStatus_Enum` — `CHECK ((("ToStatus")::text = ANY ((ARRAY['Planned'::character varying, 'Completed'::character varying, 'Cancelled'::character varying])::text[])))`

## `Voyages`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `BoatId` | uuid | hayır |  |
| `BoatRentalTypeId` | uuid | evet |  |
| `VoyageType` | character varying | hayır |  |
| `Status` | character varying | hayır |  |
| `StartsAt` | timestamp with time zone | hayır |  |
| `EndsAt` | timestamp with time zone | hayır |  |
| `DepartureDate` | date | hayır |  |
| `IsExclusive` | boolean | hayır |  |
| `Capacity` | integer | hayır |  |
| `SoldSeats` | integer | hayır |  |
| `MinPassengers` | integer | evet |  |
| `BlockReason` | character varying | evet |  |
| `CancellationReason` | character varying | evet |  |
| `CancelledAt` | timestamp with time zone | evet |  |
| `CreatedAt` | timestamp with time zone | hayır |  |
| `UpdatedAt` | timestamp with time zone | hayır |  |
| `DiverCapacity` | integer | evet |  |
| `SoldDivers` | integer | hayır | `0` |
| `BlockOwner` | character varying | evet |  |

Kısıtlar:

- `CK_Voyages_BlockOwnerRequired` — `CHECK ((((("VoyageType")::text = 'Block'::text) AND ("BlockOwner" IS NOT NULL)) OR ((("VoyageType")::text <> 'Block'::text) AND ("BlockOwner" IS NULL))))`
- `CK_Voyages_CancellationReason_Enum` — `CHECK ((("CancellationReason" IS NULL) OR (("CancellationReason")::text = ANY ((ARRAY['Weather'::character varying, 'MinPassengersNotMet'::character varying, 'OwnerCancelled'::character varying, 'CustomerCancelled'::character varying, 'OfferExpired'::character varying, 'Other'::character varying])::text[]))))`
- `CK_Voyages_DiverCapacity` — `CHECK ((("DiverCapacity" IS NULL) OR ("DiverCapacity" >= 0)))`
- `CK_Voyages_RentalTypeRequired` — `CHECK ((((("VoyageType")::text = 'Block'::text) AND ("BoatRentalTypeId" IS NULL)) OR ((("VoyageType")::text <> 'Block'::text) AND ("BoatRentalTypeId" IS NOT NULL))))`
- `CK_Voyages_SoldDivers` — `CHECK ((("SoldDivers" >= 0) AND (("DiverCapacity" IS NULL) OR ("SoldDivers" <= "DiverCapacity"))))`
- `CK_Voyages_SoldSeats` — `CHECK ((("SoldSeats" >= 0) AND ("SoldSeats" <= "Capacity")))`
- `CK_Voyages_Status_Enum` — `CHECK ((("Status")::text = ANY ((ARRAY['Planned'::character varying, 'Completed'::character varying, 'Cancelled'::character varying])::text[])))`
- `CK_Voyages_TimeRange` — `CHECK (("StartsAt" < "EndsAt"))`
- `CK_Voyages_VoyageType_Enum` — `CHECK ((("VoyageType")::text = ANY ((ARRAY['Sale'::character varying, 'Block'::character varying, 'Offer'::character varying])::text[])))`
- `EX_Voyages_NoOverlapPerBoat` — `EXCLUDE USING gist ("BoatId" WITH =, tstzrange("StartsAt", "EndsAt", '[)'::text) WITH &&) WHERE ((("Status")::text <> 'Cancelled'::text))`

## `WeatherCancellations`

| kolon | tip | boş | varsayılan |
|---|---|---|---|
| `Id` | uuid | hayır | `uuidv7()` |
| `VoyageId` | uuid | hayır |  |
| `DeclaredByUserId` | uuid | hayır |  |
| `DeclaredAt` | timestamp with time zone | hayır |  |
| `Reason` | character varying | hayır |  |
| `AlternativeOffered` | boolean | hayır |  |
| `AlternativeAccepted` | boolean | evet |  |

