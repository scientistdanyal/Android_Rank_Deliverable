USE [master]
GO
/****** Object:  Database [AndroidRank]    Script Date: 4/27/2024 6:23:30 AM ******/
CREATE DATABASE [AndroidRank]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'AndroidRank', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\AndroidRank.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'AndroidRank_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\AndroidRank_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [AndroidRank] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [AndroidRank].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [AndroidRank] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [AndroidRank] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [AndroidRank] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [AndroidRank] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [AndroidRank] SET ARITHABORT OFF 
GO
ALTER DATABASE [AndroidRank] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [AndroidRank] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [AndroidRank] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [AndroidRank] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [AndroidRank] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [AndroidRank] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [AndroidRank] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [AndroidRank] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [AndroidRank] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [AndroidRank] SET  DISABLE_BROKER 
GO
ALTER DATABASE [AndroidRank] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [AndroidRank] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [AndroidRank] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [AndroidRank] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [AndroidRank] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [AndroidRank] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [AndroidRank] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [AndroidRank] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [AndroidRank] SET  MULTI_USER 
GO
ALTER DATABASE [AndroidRank] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [AndroidRank] SET DB_CHAINING OFF 
GO
ALTER DATABASE [AndroidRank] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [AndroidRank] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [AndroidRank] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [AndroidRank] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [AndroidRank] SET QUERY_STORE = ON
GO
ALTER DATABASE [AndroidRank] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [AndroidRank]
GO
/****** Object:  Table [dbo].[Applications]    Script Date: 4/27/2024 6:23:31 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Applications](
	[package_name] [varchar](255) NOT NULL,
	[dev_id] [varchar](255) NULL,
	[title] [varchar](255) NULL,
	[category] [varchar](255) NULL,
	[price] [varchar](50) NULL,
	[total_rating] [varchar](50) NULL,
	[growth_30] [varchar](50) NULL,
	[growth_60] [varchar](50) NULL,
	[average_rating] [varchar](50) NULL,
	[installs_achieved] [varchar](50) NULL,
	[installs_estimated] [varchar](50) NULL,
	[star_5] [varchar](50) NULL,
	[star_4] [varchar](50) NULL,
	[star_3] [varchar](50) NULL,
	[star_2] [varchar](50) NULL,
	[star_1] [varchar](50) NULL,
	[rank] [bigint] NULL,
	[id] [bigint] IDENTITY(1,1) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Developers]    Script Date: 4/27/2024 6:23:31 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Developers](
	[dev_id] [varchar](255) NULL,
	[applications] [varchar](50) NULL,
	[title] [varchar](255) NULL,
	[country] [varchar](50) NULL,
	[address] [varchar](255) NULL,
	[web] [varchar](255) NULL,
	[rank] [bigint] NULL,
	[total_rating] [varchar](50) NULL,
	[average_rating] [varchar](50) NULL,
	[installs] [varchar](50) NULL,
	[id] [bigint] IDENTITY(1,1) NOT NULL,
 CONSTRAINT [PK__Develope__3213E83FB7D87AE2] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [unique_package_name]    Script Date: 4/27/2024 6:23:31 AM ******/
ALTER TABLE [dbo].[Applications] ADD  CONSTRAINT [unique_package_name] UNIQUE NONCLUSTERED 
(
	[package_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [unique_dev_id]    Script Date: 4/27/2024 6:23:31 AM ******/
ALTER TABLE [dbo].[Developers] ADD  CONSTRAINT [unique_dev_id] UNIQUE NONCLUSTERED 
(
	[dev_id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [AndroidRank] SET  READ_WRITE 
GO
